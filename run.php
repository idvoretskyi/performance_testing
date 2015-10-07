#!/usr/bin/php5
<?php

if ($argc != 4) {
    echo "Format: " . $argv[0] . " <servers> <clients> <workload>\n";
    exit(1);
}

// ========= CONFIGURATION =========

$servers = explode(",", $argv[1]);
$serverPort = 28015;
$clients = explode(",", $argv[2]);
$sshUser = "root";

$extraArgs = "";

if ($argv[3] == "c") {
    // For workload "c": Run 200 million operations
    $workload = "c";
    $totalOpcount = 200000000;
} else if ($argv[3] == "a") {
    // For workload "a": Run 50 million operations
    $workload = "a";
    $totalOpcount = 50000000;
} else if ($argv[3] == "c-outdated") {
    // For workload "c": Run 200 million operations
    $workload = "c";
    $totalOpcount = 200000000;
    $extraArgs .= " -p rethinkdb.readmode=outdated";
} else {
    echo "Unrecognized workload " . $argv[3] . "\n";
    exit(1);
}

echo "Running workload \"$workload\" with $totalOpcount operations.\n";

$recordCount = 25000000;

$durability = "hard";

$totalThreads = 128 * count($servers);

$ycsbHome = "~/YCSB";

// ========= /CONFIGURATION =========


$threadsPerClient = $totalThreads / count($clients);
$opcountPerClient = $totalOpcount / count($clients);
$hosts = implode(",", $servers);
$ycsbCmd = "$ycsbHome/bin/ycsb run rethinkdb -P $ycsbHome/workloads/workload$workload -p operationcount=$opcountPerClient -p recordcount=$recordCount -p rethinkdb.host=$hosts -p rethinkdb.port=$serverPort -p rethinkdb.durability=$durability $extraArgs -threads $threadsPerClient";

echo $ycsbCmd . "\n";

$runCmd = "read -p Wait && $ycsbCmd";

// Kill any remaining clients
foreach ($clients as $client) {
    system("ssh -oStrictHostKeyChecking=no -l $sshUser $client killall java");
}

// Launch $runCmd on each client via SSH. They will wait for a key input before actually
// starting the workload.
$procs = array();
$inPipes = array();
system("rm -r results");
@mkdir("results");
foreach ($clients as $client) {
    $sshCmd = "ssh -l $sshUser $client \"bash -c '$runCmd'\"";
    $descriptorspec = array(
       0 => array("pipe", "r"), // stdin
       1 => array("file", "results/$client.out", "w"), // stdout
       2 => array("file", "results/error-$client.err", "w") // stderr
    );
    $pipes = null;
    echo "Connecting to $client\n";
    $proc = proc_open($sshCmd, $descriptorspec, $pipes);
    if ($proc === false) die("Failed to open process");
    $procs[] = $proc;
    $inPipes[] = $pipes[0];
}

sleep(15);

// Ok, now launch the workload on each client:
echo "Running workload... ";
foreach ($inPipes as $p) {
    fwrite($p, "\n");
}

// Wait for the commands to finish
foreach ($procs as $p) {
    $res = proc_close($p);
    if ($res != 0) {
        echo "Process returned error code $res\n";
    }
}
echo "done\n";

// Merge the results
system("./ycsb_output_parser.py -d results -o results");

@mkdir("archive");
system("cp -r results archive/" . $argv[3] . "-" . count($servers) . "-$totalOpcount-" . date("c"));

?>
