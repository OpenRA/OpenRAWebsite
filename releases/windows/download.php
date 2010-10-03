<?php
	$target = file_get_contents("latest.txt");
	header("Refresh: 10; url=$target"); 
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
	<title>OpenRA - Download for Linux</title>
	<link rel="Stylesheet" type="text/css" href="/openra.css" />
	<!--[if IE 7]>
			<link rel="stylesheet" type="text/css" href="/ie7.css">
	<![endif]-->
</head>
<body>
	<div id="header" class="bar">
		<h1>
			<img src="/soviet-logo.png" alt="Logo" />OpenRA</h1>
	</div>
	<div id="main">
		<div id="menu">
			<span class="links"><a href="/index.html">Home</a></span> 
			<span class="links"><a href="/footage.html">Gameplay Footage</a></span> 
			<span class="links"><a href="/mods.html">Mods</a></span> 
			<span class="links"><a href="/getinvolved.html">Get Involved</a></span>
			<span class="links"><a href="http://www.sleipnirstuff.com/forum/viewforum.php?f=80">Forum</a></span>
			<span class="links"><a href="irc://irc.freenode.net/openra">IRC</a></span>
			<span class="links"><a href="http://twitter.com/openRA">Twitter</a></span>
		</div>
		<div id="singlecolumn">
			<h2>Downloading OpenRA for Windows</h2>
			<p>
				Thank you for downloading OpenRA for Windows. Your download will begin in 10 seconds.
				Click <?php print("<a href=\"$target\">here</a>"); ?> if it does not begin.
			</p>
			<p>
				When trying to report a crash to the developers, please include your exception.log file in your report. It can be found in My Documents/OpenRA/Logs
			</p>
			<p>
				When running a server, make sure you have <a href="http://portforward.com/">forwarded the port</a> on your router that the server is running on.
				The default port is 1234.
			</p>
		</div>
	</div>
	<div id="footer" class="bar">
		<p id="trademarks">
			<img src="/soviet-logo.png" alt="OpenRA Logo" height="70px" style="float: right; margin-right: 10px" />
			Command &amp; Conquer and Command &amp; Conquer Red Alert are trademarks or registered
			trademarks of Electronic Arts Inc.in the U.S. and/or other countries.<br />
			Windows is a registered trademark of Microsoft Corporation in the United States
			and other countries.<br />
			Mac OS X is a trademark of Apple Inc., registered in the U.S. and other countries.<br />
			Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.<br />
			Mono is a registered trademark of Novell, Inc. in the United States and other countries.<br />
		</p>
	</div>
</body>