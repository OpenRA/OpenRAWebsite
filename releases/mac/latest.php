<?php
$file = file_get_contents("../../downloads.txt");
file_put_contents("../../downloads.txt", $file + 1);
header("Location: download.php");
?>
