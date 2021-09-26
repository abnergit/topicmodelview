<?php
if(isset($_GET['termos'])){
	$termos = $_GET['termos'];
}



if(isset($termos)){
	#codigo por termos
}else{
	?>
	<!-- Card -->
	<div class="card mb-4">
		<!-- Card Header -->
		<header class="card-header">
			<h2 class="h4 card-header-title">Termos</h2>
		</header>
		<!-- End Card Header -->

		<!-- Card Body -->
		<div class="card-body py-0">
			<!-- Flushed List Group -->
			<ul class="list-group list-group-flush">
				<?php
				
			
					$hoje = date("Y-m-d");
					$sql = "SELECT * FROM terms LIMIT 5;";
				
					$result = $conexao->query($sql);
					while($row = $result->fetch_assoc()) { 
				
				
				
				
				?>
				<!-- List Group Item -->

				<li class="list-group-item border-0">
					<a class="media link-dark align-items-center" href="?deputado=<?php echo $row['iddeputado'] ?>">
						<!-- Avatar >
						<img class="u-avatar-sm rounded-circle mr-3" src="../fotos/<?php echo $row['iddeputado'] ?>.jpg" alt="Image description">
						<!-- End Avatar -->

						<!-- Title and Short Text -->
						<div class="media-body">
							<h4 class="font-weight-normal pt-1 mb-1"><?php echo $row['title'] ?></h4>
							<!--div class="text-muted"><?php echo $row['email'] ?></div-->
						</div>
						<!-- End Title and Short Text -->
					</a>
				</li>
				<!-- End List Group Item -->
				<?php } 
				
				
				
				?>

			</ul>
			<!-- End Flushed List Group -->
		</div>
		<!-- End Card Body -->

		<!-- Card Footer -->
		<footer class="card-footer">
			<a class="font-weight-semi-bold" href="/topicmodel/termos/">Ver 1000...</a>
		</footer>
		<!-- End Card Footer -->
	</div>
	<!-- End Card -->
<?php } ?>