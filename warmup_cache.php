#!/usr/bin/php5
<?php
include 'rdb/rdb.php';

if ($argc != 2) {
    echo "Format: " . $argv[0] . " <servers>\n";
    exit(1);
}

$servers = explode(",", $argv[1]);
$serverPort = 28015;

$conns = array();
foreach ($servers as $server) {
    $conns[] = r\connect($server, $serverPort);
}

foreach ($conns as $conn) {
    r\db('ycsb')->table('usertable')->map(r\row())->count()->run($conn, array("read_mode" => "_debug_direct", "noreply" => true));
}

// Run it a second time
foreach ($conns as $conn) {
    $conn->noreplyWait();
    r\db('ycsb')->table('usertable')->map(r\row())->count()->run($conn, array("read_mode" => "_debug_direct", "noreply" => true));
}

foreach ($conns as $conn) {
    $conn->noreplyWait();
    $conn->close();
}

?>
