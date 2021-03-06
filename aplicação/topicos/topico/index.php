<!DOCTYPE html>
<?php


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
	$file_handle = fopen("/var/www/html/topicmodel/corpus/doc_$titulo", "r");
	$retorno = "";
	while (!feof($file_handle)) {
		$retorno = $retorno.fgets($file_handle);
	}
	fclose($file_handle);
	return substr($retorno, 0, 500) . "...";
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

	<!-- Components Vendor Styles -->
	<link rel = "stylesheet" href = "../../assets/vendor/themify-icons/themify-icons.css">
	<link rel = "stylesheet" href = "../../assets/vendor/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.css">

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
				<div class = "row">
					
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
								<div   class = "media link-dark align-items-center" href = "?deputado=<?php echo $row['id'] ?>">
									<?php
									$sql    = "SELECT * FROM topic_term where topic = $topico limit 100";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										$palavra = get_termo($conexao, $row['term']);
										echo $palavra . "<br>";
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
									$sql    = "SELECT * FROM doc_topic where topic = $topico order by score desc limit 20";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										#$palavra = get_termo($conexao, $row['term']);
										#echo $palavra . "<br>";
										$texto = imprime_texto($row['doc']);
										$id_texto = $row['doc'];
										echo "<a href='/topicmodel/documentos/documento/?id=$id_texto'><b>Texto ".$row['doc']."</b></a>";
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
									$sql    = "SELECT * FROM topic_topic where topic_a = $topico order by score desc";
									$result = $conexao->query($sql);
									while ($row = $result->fetch_assoc()) {
										$palavra = get_topic_name($conexao, $row['topic_b']);
										echo "<a href='/topicmodel/topicos/topico/?id=".$row['topic_b']."' >";
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

	<!-- Global Vendor -->
	<script src = "../../assets/vendor/jquery/dist/jquery.min.js"></script>
	<script src = "../../assets/vendor/jquery-migrate/jquery-migrate.min.js"></script>
	<script src = "../../assets/vendor/popper.js/dist/umd/popper.min.js"></script>
	<script src = "../../assets/vendor/bootstrap/dist/js/bootstrap.min.js"></script>

	<!-- Plugins -->
	<script src = "../../assets/vendor/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.concat.min.js"></script>

	<!-- Initialization  -->
	<script src = "../../assets/js/sidebar-nav.js"></script>
	<script src = "../../assets/js/main.js"></script>
</body>
<!-- End Body -->

</html>

<?php $conexao->close(); ?>