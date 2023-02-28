<?php
$GLOBALS['uniqueid'] = $_POST['uniq_id'];
$GLOBALS['name'] = $_POST['u_name'];
$email = $_POST['emails'];
$number = $_POST['u_number'];
$uname = $_POST['username'];
$degree = $_POST['u_degree'];
$semester = $_POST['u_semester'];
$cgpa = $_POST['u_cgpa'];
$address = $_POST['address'];
$resume = $_POST['u_resume'];
$linkedin = $_POST['linkedIn'];
$github = $_POST['git_hub'];
$marksheet10 = $_POST['marksheet10'];
$marksheet12 = $_POST['marksheet12'];
$certificate = $_POST['certificate'];


#database connection
 define("DB_HOST", "localhost");
 define("DB_USER", "root");
 define("DB_PASSWORD", "");
 define("DB_DATABASE", "studentdb");
 $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE);
if(!$conn)
 { echo "$conn->connect_error";
die('Connection Failed : '.$conn->connect_error);
 }
else{
 $stmt = "INSERT INTO studentdetails(uniqueid,name,number,uname,degree,semester,cgpa,resume,linkedin,github,address,email,marksheet10,marksheet12,certificate)
 VALUES('$uniqueid','$name','$number','$uname','$degree','$semester','$cgpa','$resume','$linkedin','$github','$address','$email','$marksheet10','$marksheet12','$certificate')";

if(mysqli_query($conn, $stmt))
{
 echo "Registration Successfull..";
}
else{ 
echo "Error: ".mysqli_error($conn);
}
mysqli_close($conn);
 }

$target_dir = "newImages/";  #folder where the image that is uploaded will get stored
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
  $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
  if($check !== false) {
    echo "\r\n File is an image - " . $check["mime"] . ".";
    $uploadOk = 1;
  } else {
    echo "\r\n File is not an image.";
    $uploadOk = 0;
  }
}

// Check if file already exists
if (file_exists($target_file)) {
  echo "\r\n Sorry, file already exists.";
  $uploadOk = 0;
}

// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
  echo "\r\n Sorry, your file is too large.";
  $uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
  echo "\r\nSorry, only JPG, JPEG, PNG & GIF files are allowed.";
  $uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "\r\nSorry, your file was not uploaded.";

// if everything is ok, try to upload file
} else {
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
    } 
    else {
    echo "\r\nSorry, there was an error uploading your file.";
  }
}
?>

<?php
#running the encoding.py file to add the new encodings of the uploaded image
$command = escapeshellcmd('python Encodings.py');
$output = shell_exec($command);

#redirecting the page to scanFace.html after successful registration
echo '<script>alert("Registration Successful"); window.location="scanFace.html"</script>';
exit();
 ?>
