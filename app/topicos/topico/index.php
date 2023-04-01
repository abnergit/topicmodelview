<!DOCTYPE html>
<?php
require_once("../../conexao.php");


if (isset($_GET['id']) and is_numeric($_GET['id'])) {
	$topico = $_GET['id'];
} else {
	#REDIRECT EM TENTATIVA DE INJECTION ATRAVÉS DA URL
?>
	<script>
		location.replace("../");
	</script>
<?php
}

function imprime_texto($titulo, $conexao)
{
	$eRedacao = False;
	$titulo = addslashes($titulo);
	$sql = "SELECT * FROM docs where id = $titulo";
	$result = $conexao->query($sql);
	$row = mysqli_fetch_assoc($result);
	$titulo = $row['title'];
	if(strpos($titulo, "doc") !== false){
		$file_handle = fopen("../../corpus/$titulo", "r");
		$retorno = "";
		while (!feof($file_handle)) {
			$retorno = $retorno.fgets($file_handle);
		}
	}else{
		$file_handle = fopen("../../redações/$titulo", "r");
		$retorno = "";
		while (!feof($file_handle)) {
			$retorno = $retorno.fgets($file_handle);
		}
		$eRedacao = True;
	}
	fclose($file_handle);
	return array(substr($retorno, 0, 500) . "	...", $eRedacao);
}


require_once("../../conexao.php");

function get_termo($conexao, $id)
{
	$sql = "SELECT * FROM terms where id = $id;";

	$result = $conexao->query($sql);
	$row    = $result->fetch_array();
	return $row['title'];
}
function get_topic_name($conexao, $id)
{
	$sql = "SELECT * FROM topics where id = $id;";
	
	$result = $conexao->query($sql);
	$row    = $result->fetch_array();
	return $row['title'];
}
?>
<html lang = "en" class = "no-js">
<!-- Head -->

<head>
	<title>Documentos</title>

	<!-- Meta -->
	<meta charset    = "utf-8">
	<meta name       = "viewport" content        = "width=device-width, initial-scale=1, shrink-to-fit=no">
	<meta http-equiv = "x-ua-compatible" content = "ie=edge">

	<!-- Favicon -->
	<link rel = "shortcut icon" href = "../../favicon.png" type = "image/x-icon">

	<!-- Web Fonts -->
	<link href = "//fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel = "stylesheet">

	<!-- Theme Styles -->
	<link rel = "stylesheet" href = "../../css/theme.css">
</head>
<!-- End Head -->

<!-- Body -->

<body>
	<!-- Header (Topbar) -->

	<?php include("../../header.html"); ?>

	<!-- End Header (Topbar) -->

	<!-- Main -->
	<main class = "u-main">
		<!-- Sidebar -->
		<?php include("../../sidebar.html"); ?>
		<!-- End Sidebar -->

		<!-- Content -->
		<div class = "u-content">
			<!-- Content Body -->
			<div class = "u-body">
			<div class = "titulos" align = "center">
					<?php echo "<b>".get_topic_name($conexao, $_GET['id'])."</b>"; ?>
				</div>
				<div class = "row_topic">
					
					<div class = "card mb-5" align = "left">
						<!-- Card Header -->
						<header class = "card-header">
						<h2     class = "h4 card-header-title"> Termos relacionados </h2>
						</header>
						<!-- End Card Header -->
						<!-- Card Body -->
						<div class = "card-body py-0">
							<!-- Flushed List Group -->
							<ul class = "list-group list-group-flush">

								<!-- List Group Item -->

								<!--li class = "list-group-item border-0"-->
								<div   class = "media link-dark align-items-center" href = "#">
									<?php
									$sql    = "SELECT * FROM topic_term where topic = $topico limit 100";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										$palavra = get_termo($conexao, $row['term']);
										$score = $row['score'];
										echo $palavra . " - ($score) <br>";
									}
									?>

									</a>
									<!--/li-->
									<!-- End List Group Item -->
								</div>

							</ul>
							<!-- End Flushed List Group -->
						</div>
						<!-- End Card Body -->
					</div>
					<!-- End Card -->
					<!-- FINAL PALAVRAS -->

					<!-- INICIO DOCUMENTOS RELCIONADOS -->
					<div class = "col-md-7 col-lg-7" align = "center">
						<!-- Card Header -->
						<header class = "card-header">
						<h2     class = "h4 card-header-title"> Textos relacionados </h2>
						</header>
						<!-- End Card Header -->
						<!-- Card Body -->
						<div class = "py-0">
							<!-- Flushed List Group -->
							<ul class = "list-group list-group-flush">
									<?php
									$sql    = "SELECT dt.doc as doc, dt.score, docs.title  FROM doc_topic as dt, docs where docs.id = dt.doc and topic = $topico and dt.score > 0 and docs.title like 'red%' order by score desc limit 20";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										#$palavra = get_termo($conexao, $row['term']);
										#echo $palavra . "<br>";
										$imprime_retorno = imprime_texto($row['doc'], $conexao);
										$texto = $imprime_retorno[0];
										$doc = $row['title'];
										$id = $row['doc'];
										echo "<a href='/documentos/documento/?id=$id&doc=$doc' style='color: red;'><b>Redação ".$row['title']." - Score [".$row['score']."]</b></a>";
										echo "<textarea readonly rows='3'>";
										echo $texto;
										echo "</textarea>";
									}
									$sql    = "SELECT dt.doc as doc, dt.score, docs.title  FROM doc_topic as dt, docs where docs.id = dt.doc and topic = $topico order by score desc limit 20";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										#$palavra = get_termo($conexao, $row['term']);
										#echo $palavra . "<br>";
										$imprime_retorno = imprime_texto($row['doc'], $conexao);
										$texto = $imprime_retorno[0];
										$doc = $row['title'];
										$id = $row['doc'];
										echo "<a href='/documentos/documento/?id=$id&doc=$doc'><b>Documento ".$row['doc']." - Score [".$row['score']."]</b></a>";
										echo "<textarea readonly rows='3'>";
										echo $texto;
										echo "</textarea>";
									}
									?>
							</ul>
							<!-- End Flushed List Group -->
						</div>
						<!-- End Card Body -->
					</div>
					<!-- End Card -->
					<!-- FINAL DOCUMENTOS -->
					
					<!-- INICIO TÓPICOS RELCIONADOS -->
					<div class = "card mb-5" align = "center">
						<!-- Card Header -->
						<header class = "card card-header">
						<h2     class = "h4 card-header-title"> Tópicos relacionados </h2>
						</header>
						<!-- End Card Header -->
						<!-- Card Body -->
						<div class = "py-0">
							<!-- Flushed List Group -->
							<ul class = "list-group list-group-flush">
									
									<?php
									$sql    = "SELECT * FROM topic_topic where topic_a = $topico order by score asc";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										$palavra = get_topic_name($conexao, $row['topic_b']);
										echo "<a href='/topicos/topico/?id=".$row['topic_b']."' >";
										echo $palavra;
										echo "</a><br>";
										
									}
									?>
							</ul>
							<!-- End Flushed List Group -->
						</div>
						<!-- End Card Body -->
					</div>
					<!-- End Card -->
					<!-- FINAL POSTS -->





				</div>
			</div>
			<!-- End Content Body -->

			<?php include("../../footer.html") ?>
		</div>
		<!-- End Content -->
	</main>
	<!-- End Main -->

</body>
<!-- End Body -->

</html>

<?php $conexao->close(); ?>
