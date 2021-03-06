<?php session_start();?>

<html>
<link rel="stylesheet" type="text/css" href="css/material.css" />
	<title>Tracker - Film</title>
	<body>
		<?php
			set_include_path("{$_SERVER['DOCUMENT_ROOT']}");
			require_once('config.php');
			require_once('View/Util.php');
            $id = $_GET["id"];
			$uid = 0;
			$json = file_get_contents("{$GLOBALS["ip"]}index.php?type=films&id={$id}"); 
			$movie = json_decode($json, true);
            if(!$movie){
                $_SESSION["message"] = "No Film with that ID";
			    $url = "{$GLOBALS['ip']}View/displayMessage.php";
			    header( "Location: $url" );
            }
			$id = $movie['id'];
			$db = new SQLite3($_SERVER['DOCUMENT_ROOT'].'/database.db'); 
			$util = new Util();
			
			$genre = substr($movie['genre'],8,-2);
			$genre = str_replace("+",", ",$genre);
			$type = "films";
            include_once("View/navbar.php");
		?>
			<div class='show_container'>
				<div class='image' style='float:left'>
	                <?php echo "<img class='cover' src='" . $movie['image'] . "'>";
                        echo "<div class='show_info'>";
                            echo "<p class='show_info'>" . $movie['runtime'] . " minutes</p>";
                            echo "<p class='show_info'>Age: ".$movie['age']."</p>";
                            echo "<p class='show_info double_info'>".$movie['rating']." Stars</p>";
                            
							echo "<p class='show_info double_info'>" . str_replace("+", " ", $movie['genre']) . "</p>";
                        if(!$util->rowExists($db,"track","films",$id)){
							echo "<form action='../Model/track.php?type=films&id={$id}' method='post'>";
								echo "<label for='track'><p class='show_info button'>Track</p></label>";
								echo "<input style='position:absolute;visibility:hidden' id='track' type='submit' name='formSubmit' value='Track' />";
							echo "</form>";
						} else {
							echo "<form action='../Model/track.php?type=films&id={$id}' method='post'>";
								echo "<a href'#'><label for='track'><p class='show_info button'>Untrack</p></label></a>";
								echo "<input style='position:absolute;visibility:hidden' id='track' type='submit' name='formSubmit' value='Untrack' />";
							echo "</form>";
						}
						
						// Likes
						if(!$util->rowExists($db,"likes","films",$id)){
							// Track
							echo "<form action='../Model/insertLikes.php?type=films&id={$id}' method='post'>";
								echo "<label for='like'><p class='show_info button'>Like</p></label>";
								echo "<input style='position:absolute;visibility:hidden' id='like' type='submit' name='formSubmit' value='like' />";
							echo "</form>";  
						} else {
							echo "<form action='../Model/insertLikes.php?type=films&id={$id}' method='post'>";
								echo "<label for='like'><p class='show_info button'>Unlike</p></label>";
								echo "<input style='position:absolute;visibility:hidden' id='like' type='submit' name='formSubmit' value='like' />";
							echo "</form>";  
						}
						echo "</div>"; 
						?>
			    </div>
			    <div class='info'>
					<?php echo "<div class='title'><h2 class='title'>" . $movie['name'] . "</h2></div>";?>
					<?php echo "<div class='summary'><p class='summary'>" . $movie['synopsis'] . "</p></div>";
                    echo "<div class='summary'><p class='summary' style='text-align:center'><b>Release Date:</b> " . $movie['date'] . "</p></div>";
				    echo "<div class='summary'><p class='summary'><b>Starring:</b> " . $movie['starring'] . "</p></div>";
				    echo "<div class='summary'><p class='summary' ><b>Directed By:</b> " . $movie['director'] . "</p></div>";?>
                </div>
			</div>
		<!--<div style='margin-left:14%;float:left'>
			<?php /* if(!$util->rowExists($db,"track"))
			{
				echo "<form action='../Model/track.php?type={$type}&id={$id}' method='post'>";
    					echo "Would you like to track this film?";
    					echo "<input type='submit' name='formSubmit' value='Track' />";
				echo "</form>";
			}else {
				echo "<form action='../Model/track.php?type={$type}&id={$id}' method='post'>";
    					echo "Would you like to untrack this film?";
    					echo "<input type='submit' name='formSubmit' value='Untrack' />";
				echo "</form>";
			}*/?>
		</div>
		<div style='float:right;margin-right:180px'>
			<?php /*if(!$util->rowExists($db,"likes"))
            {
                echo "<form action='../Model/insertLikes.php?type={$type}&id={$id}' method='post'>";
        	        echo "Like Film to use for Recommendations!";
        			echo "<input type='checkbox' name='film[]' value='".$movie['name']."&&&".$movie['id']."&&&".$movie['image']."'>";
                    echo "<input type='submit' value='Submit'>";   
                echo "</form>";  
            }else{
                echo "<form action='../Model/insertLikes.php?type={$type}&id={$id}' method='post'>";
        	        echo "Don't like it anymore?";
        			echo "<input type='checkbox' name='film[]' value='".$movie['name']."&&&".$movie['id']."&&&".$movie['image']."'>";
                    echo "<input type='submit' value='Unlike'>"; 
                echo "</form>"; 
            }*/?>
			</form>
		</div>	-->
	</body>
</html>
