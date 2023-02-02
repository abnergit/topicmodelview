<?php
function get_termo($conexao, $id){
	$sql = "SELECT * FROM terms where id = $id;";
		
	$result = $conexao->query($sql);
	$row = $result->fetch_array();
	return $row['title'];

}
if(isset($_GET['topico'])){
	$topico = $_GET['topico'];
}



if(isset($topico)){
	#codigo por topico
}else{
				
			
	$hoje = date("Y-m-d");
	$sql = "SELECT * FROM terms limit 1000;";
		
	$result = $conexao->query($sql);
	while($row = $result->fetch_assoc()) { 
			
			
			
			
	?>
	<!-- Card -->
	<div class="card mb-5">
		<!-- Card Header -->
		<header class="card-header">
			<h2 class="h4 card-header-title">Termo <?php echo $row['id'] ?></h2>
		</header>
		<!-- End Card Header -->

		<!-- Card Body -->
		<div class="card-body py-0">
		 <?php echo $row['title']; ?>
		</div>
		<!-- End Card Body -->
	</div>
	<!-- End Card -->
<?php }

} ?>