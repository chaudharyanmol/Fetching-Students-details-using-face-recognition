<?php
$user = $_POST['user_name'];
$pass = $_POST['u_password'];


if($user=="Admin" && $pass =="pass123")
{
  header("Location:scan_Face.html");
}

?>