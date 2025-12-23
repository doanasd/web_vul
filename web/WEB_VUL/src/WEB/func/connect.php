<?php
    $servername = "db";
    $usname = "root";
    $pass = "123asd";
    $database = "mixue";

    $conn = new mysqli($servername, $usname, $pass, $database);
    if ($conn->connect_error){
        die("Connection failed: ".$conn->connect_error);
    } 
?>