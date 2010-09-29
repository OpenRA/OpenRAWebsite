<?php
$latest = file_get_contents("latest.txt");
header("Location: $latest");
$file = file_get_contents("../../downloads.txt");
file_put_contents("../../downloads.txt", $file + 1);
?>
