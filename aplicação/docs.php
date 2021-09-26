<html>
<?php

function imprime_texto($titulo)
{
	$file_handle = fopen("corpus/$titulo", "r");
	$retorno = "";
	while (!feof($file_handle)) {
		$retorno = $retorno.fgets($file_handle);
	}
	fclose($file_handle);
	return substr($retorno, 0, 500) . "...";
}

?>
<!-- Card -->
<div class="card mb-5">
	<!-- Card Header -->
	<header class="card-header">
		<div class="d-flex align-items-center justify-content-between">
			<h2 class="h4 card-header-title">
				Documentos
			</h2>

		</div>

		<span class="text-muted"></span>
	</header>
	<!-- End Card Header -->

	<!-- Card Body -->
	<div class="card-body py-0">
		<p>
			<?php


			$hoje = date("Y-m-d");
			$sql  = "SELECT * FROM docs LIMIT 5;";

			$result = $conexao->query($sql);
			while ($row = $result->fetch_assoc()) {




			?>
				<!-- List Group Item -->

				<li class = "list-group-item border-0">
				<a  class = "media link-dark align-items-center" href = "?deputado=<?php echo $row['iddeputado'] ?>">
						<!-- Avatar >
											<img class = "u-avatar-sm rounded-circle mr-3" src = "../fotos/<?php echo $row['iddeputado'] ?>.jpg" alt = "Image description">
											<!-- End Avatar -->

						<!-- Title and Short Text -->
						<div class = "media-body">
						<h4  class = "font-weight-normal pt-1 mb-1"><?php echo $row['title'] ?></h4>
						<div class = "text-muted"><?php echo imprime_texto($row['title']) ?></div>
						</div>
						<!-- End Title and Short Text -->
					</a>
				</li>
				<!-- End List Group Item -->
			<?php }

			#$conexao->close();

			?>
			<!-- Attach >
									<div class = "row gutters-sm">
									<div class = "col-md-4">
									<img class = "img-fluid rounded" src = "assets/img-temp/500x280/img1.jpg" alt = "Image Description">
										</div>

										<div class = "col-md-4">
										<img class = "img-fluid rounded" src = "assets/img-temp/500x280/img2.jpg" alt = "Image Description">
										</div>

										<div class = "col-md-4">
										<img class = "img-fluid rounded" src = "assets/img-temp/500x280/img3.jpg" alt = "Image Description">
										</div>
									</div>
									<!-- End Attach -->
	</div>
	<!-- End Card Body -->

	<!-- Card Footer -->
	<!-- Card Footer -->
	<footer class="card-footer">
		<a class="font-weight-semi-bold" href="/topicmodel/documentos/">Ver 1000...</a>
	</footer>
	<!-- End Card Footer -->
	<!-- End Card Footer -->
</div>
<!-- End Card -->




</html>