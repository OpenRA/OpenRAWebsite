<?php
header("Location: download.php");
$file = file_get_contents("../../downloads.txt");
file_put_contents("../../downloads.txt", $file + 1);
?>
