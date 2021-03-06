<?php session_start();

set_include_path("{$_SERVER['DOCUMENT_ROOT']}");
require_once('config.php');
$db = new SQLite3($_SERVER['DOCUMENT_ROOT'].'/database.db');

function getNumRows(){
	$rows = $db->query("SELECT COUNT(*) as count FROM users");
	$row = $rows->fetchArray();
	$numRows = $row['count'];
	return $numRows;
}

if($_SERVER['REQUEST_METHOD'] == 'POST'){
	$username = $_POST['username'];
    $password_entered = $_POST['password'];
	
	$stmt = $db->prepare('SELECT Id,username,password FROM `users` WHERE username = :username');
	$stmt->bindValue(':username',$username,SQLITE3_TEXT);
	$result = $stmt->execute();

	$rows = $result->fetchArray();
	$id = $rows['Id'];
	$username = $rows['username'];
    $hash = $rows['password'];

	if($rows){
        if($hash == md5($password_entered)){
		    session_start();
		    $_SESSION['userID'] = $id;	
		    $_SESSION['username'] = $username;
		    $url = "{$GLOBALS['ip']}View/getFilmList.php?type=films&organise=1&page=0&order=ASC";
		    header( "Location: $url" );
        }else{
		    $_SESSION["message"] = "Incorrect password";
		    $url = "{$GLOBALS['ip']}View/displayMessage.php";
		    header( "Location: $url" );           
        }
	}else{
		$_SESSION["message"] = "Incorrect Username";
		$url = "{$GLOBALS['ip']}View/displayMessage.php";
		header( "Location: $url" );
	}
}

?>
