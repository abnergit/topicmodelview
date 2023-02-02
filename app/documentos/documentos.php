<?php
function get_termo($conexao, $id)
{
	$sql = "SELECT * FROM terms where id = $id;";

	$result = $conexao->query($sql);
	$row    = $result->fetch_array();
	return $row['title'];
}

function imprime_texto($titulo)
{
	/*
	$id          = explode("oc_", $titulo)[1];
	$file_handle = fopen("../corpus.txt", "r");
	$count       = 0;
	$retorno     = "";
	while (!feof($file_handle)) {
		$line = fgets($file_handle);
		if ($count == $id) {
			$retorno = $line;
			break;
		}
		$count++;
	}
	*/
	$file_handle = fopen("../corpus/$titulo", "r");
	$retorno = "";
	while (!feof($file_handle)) {
		$retorno = $retorno.fgets($file_handle);
	}
	fclose($file_handle);
	return substr($retorno, 0, 500) . "...";
}
if (isset($_GET['topico'])) {
	$topico = $_GET['topico'];
}



if (isset($topico)) {
	#codigo por topico
} else {


	$hoje = date("Y-m-d");
	$sql  = "SELECT * FROM docs limit 1000;";

	$result = $conexao->query($sql);
	while ($row = $result->fetch_assoc()) {

?>
		<!-- Card -->
		<div class="card mb-5">
			<!-- Card Header -->
			<header class="card-header">
				<a href="documento/?id=<?php echo $row['id'] ?>"><h2 class="h4 card-header-title">Documento <?php echo $row['id'] ?></h2></a>
			</header>
			<!-- End Card Header -->

			<!-- Card Body -->
			<div class="card-body py-0">
				<?php echo "<textarea readonly rows='11' cols='38'>".imprime_texto($row['title'])."</textarea>" ?>
			</div>
			<!-- End Card Body -->
		</div>
		<!-- End Card -->
<?php }
} ?>