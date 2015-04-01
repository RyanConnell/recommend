<?php

class Util{

 	function checkNextSeason($season,$id){
		
		$json = file_get_contents("{$GLOBALS["ip"]}Tracker/index.php?type=tv_shows&id={$id}&season={$season}");		

		if(strpos($json,'okay') !== false){
			return true;
		}else{
			return false;
		}
	}

    function nextSeason($season,$id){
        return "{$GLOBALS["ip"]}Tracker/View/getShow.php?id={$id}&season={$season}";
    }

	function checkNextPage($type,$page,$organise){
		$json = file_get_contents("{$GLOBALS["ip"]}Tracker/index.php?type={$type}&organise={$organise}&page={$page}");

		if(strpos($json,'okay') !== false){
			return $page;
		}else{
			return '0';				
		}
	}

	function checkNextLike($type,$page){
		$json = file_get_contents("{$GLOBALS["ip"]}Tracker/index.php?type={$type}&page={$page}");
		if(strpos($json,'okay') !== false){
			return $page;
		}else{
			return '0';				
		}
	}

	function rowExists($db,$table){
		$stmt = $db->prepare("SELECT userID, mediaID,mediaTable FROM `{$table}` WHERE userID = :userID AND mediaID = :mediaID AND mediaTable = :mediaTable");
		$stmt->bindValue(':mediaTable',$_GET['type'],SQLITE3_TEXT);
		$stmt->bindValue(':userID',$_SESSION['userID'],SQLITE3_INTEGER);
		$stmt->bindValue(':mediaID',$_GET['id'],SQLITE3_TEXT);
		$result = $stmt->execute();
		$row = $result->fetchArray();
		if($row){
			return true;
		}else return false;
	}
}
