<html>
<?php

function imprime_texto($titulo)
{
	$file_handle = fopen("corpus/$titulo", "r");
	$retorno     = "";
	while (!feof($file_handle)) {
		$retorno = $retorno.fgets($file_handle);
	}
	fclose($file_handle);
	return htmlspecialchars(substr($retorno, 0, 500) . "...");
}

?>
<!-- Card -->
<div class = "card mb-5">
	<!-- Card Header -->
	<header class = "card-header">
	<div    class = "d-flex align-items-center justify-content-between">
	<h2     class = "h4 card-header-title">
				Documentos
			</h2>

		</div>

		<span class = "text-muted"></span>
	</header>
	<!-- End Card Header -->

	<!-- Card Body -->
	<div class = "card-body py-0">
		<p>
			<?php


			$hoje = date("Y-m-d");
			$sql  = "SELECT * FROM docs LIMIT 5;";

			$result = $conexao->query($sql);
			while ($row = $result->fetch_assoc()) {




			?>
				<!-- List Group Item -->

				<li class = "list-group-item border-0">
				<div  class = "media link-dark align-items-center">
				
						<!-- Title and Short Text -->
						<div class = "media-body">
						<h4  class = "font-weight-normal pt-1 mb-1"><?php echo $row['title'] ?></h4>
						<div class = "text"><?php echo imprime_texto($row['title']) ?></div>
						</div>
						<!-- End Title and Short Text -->
			</div>
				</li>
				<!-- End List Group Item -->
			<?php }

			#$conexao->close();

			?>
		
	</div>
	<!-- End Card Body -->

	<!-- Card Footer -->
	<!-- Card Footer -->
	<footer class = "card-footer">
	<a      class = "font-weight-semi-bold" href = "/documentos/">Ver 1000...</a>
	</footer>
	<!-- End Card Footer -->
	<!-- End Card Footer -->
</div>
<!-- End Card -->




</html>