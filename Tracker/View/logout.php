<?php
Session_start();
Session_destroy();

set_include_path("{$_SERVER['DOCUMENT_ROOT']}");
require_once('config.php');
$url = "{$GLOBALS['ip']}/View/getFilmList.php?type=film&organise=1&page=0";
header( "Location: $url" );
?>


