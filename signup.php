<?php
header('Access-Control-Allow-Origin: *');
$email = $_POST['email'];
$password = $_POST['password'];
$name = $_POST['name'];
$gender = $_POST['gend'];

$conn = new mysqli('localhost', 'root', '', 'test');
if ($conn->connect_error) {
    die('Connection Failed: ' . $conn->connect_error);
}
$stmt = $conn->prepare("SELECT * FROM userdetails WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();
$result='';
if ($stmt->num_rows > 0) 
{
    echo "Account already exists";
}
else 
{
    $stmt = $conn->prepare("INSERT INTO userdetails (email, password, name, gender) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $email, $password, $name, $gender);
    $stmt->execute();
    echo "Account created successfully";
}
$stmt->close();
$conn->close();
?>
