<?php 


$host = "localhost"; // Local da base de dados MySQL
$usuario = "login_banco"; // Login do MySQL
$password = "senha_banco"; // Senha para conectar com o MySQL
$base = "discursos"; // Nome do Banco de Dados



$conexao = mysqli_connect($host,$usuario,$password) or die ('Não foi possível conectar: ');
$banco = mysqli_select_db($conexao, $base);
mysqli_set_charset($conexao,'utf8');


?>
