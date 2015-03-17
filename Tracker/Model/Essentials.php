<?php

class Essentials{

	public function search($db,$type,$search){

		$sql = "SELECT name,image,id,rating FROM `{$type}` WHERE name LIKE '%{$search}%' ORDER BY name DESC LIMIT 24";
		$retval = $db->query($sql);
		echo "{\"{$type}\":[";
 		$tick = 0;
 		while($row = $retval->fetchArray()){
 		    if ($tick != 0){
 			echo ",";
 		    }
 		    $tick++;
		    echo json_encode(array("status" => "okay",
		                           "name" => $row["name"],
		                           "rating" => $row["rating"],
					   "id" => $row["id"],
					   "image" => $row["image"]));
		}
 		echo "]}";
	}


	public function getMaxID(){
		$db = new SQLite3('films.db');
		$maxID = 'SELECT * FROM films ORDER BY id DESC LIMIT 1';
		$result = $db->query($maxID);
		$maxID = $result->fetchArray();
		$maxID = intval($maxID["id"]);
		return $maxID;
	}

	public function createArrayFromData($sql, $row){
		$array = array();
		
		$data = explode("SELECT ", $sql)[1];
		$data = explode(" FROM", $data)[0];
		$data = explode(",", $data);
		
		$array["status"] = "okay";
		foreach ($data as $var_name) {
			$array[$var_name] = $row[$var_name];
		}
		
		return $array;
	}

	public function getList($organise,$page,$type,$db){
		$pageParam = intval($page);
		$offset = $pageParam * 24;
		$maxPage = floor($this->getMaxID() / 24);
		
		if($type == "films"){
			if($organise == "rating"){
				$sql = "SELECT name,date,image,rating,id FROM `{$type}` ORDER BY {$organise} DESC LIMIT 24 OFFSET {$offset}";
			} else if($organise == "date"){
				$sql = "SELECT name,date,rating,image,id FROM `{$type}` ORDER BY {$organise} LIMIT 24 OFFSET {$offset}";
			} else {
				$sql = "SELECT name,date,image,rating,id FROM `{$type}` ORDER BY {$organise} LIMIT 24 OFFSET {$offset}";
			}		
		}else {
			if($organise == "name"){
				$sql = "SELECT name,image,rating,id FROM `{$type}` ORDER BY {$organise} LIMIT 24 OFFSET {$offset}";
			} else{
				$sql = "SELECT name,image,rating,id FROM `{$type}` ORDER BY {$organise} DESC LIMIT 24 OFFSET {$offset}";
			}		
		}	

		$retval = $db->query($sql);
		echo "{\"{$type}\":[";
		$tick = 0;
		while($row = $retval->fetchArray()){
		    if ($tick != 0){
			echo ",";
		    }
		    $tick++;
		    echo json_encode($this->createArrayFromData($sql, $row));
		}
		echo "]}";

	}

}
