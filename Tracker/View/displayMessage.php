<?php session_start();
set_include_path("{$_SERVER['DOCUMENT_ROOT']}");

?>

<html>
<link rel="stylesheet" type="text/css" href="css/message.css" />
	<title>Tracker - Message</title>
	<body>
	<?php
		set_include_path("{$_SERVER['DOCUMENT_ROOT']}");
		require_once('Tracker/config.php');
        include_once('Tracker/View/navbar.php');

		echo "<div class='show_container'>";
			if($_SESSION["message"]){
				$msg = $_SESSION["message"];
				echo $msg;
			}else {
				echo "Username is already in use, please try another!";
			}
			
		echo "</div>";
	?>
	</body>
</html>
