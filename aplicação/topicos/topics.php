<?php
function get_termo($conexao, $id)
{
	$sql    = "SELECT * FROM terms where id = $id;";
	$result = $conexao->query($sql);
	$row    = $result->fetch_array();
	return $row['title'];
}
if (isset($_GET['topico'])) {
	$topico = $_GET['topico'];
}



if (isset($topico)) {
	#codigo por topico
} else {


	$hoje = date("Y-m-d");
	$sql  = "SELECT * FROM topics";

	$result = $conexao->query($sql);
	while ($row = $result->fetch_assoc()) {




?>
		<!-- Card -->
		<div class = "card mb-5">
			<!-- Card Header -->
			<header class = "card-header">
			<a      href  = "topico/?id=<?php echo $row['id'] ?>">
			<h2     class = "h4 card-header-title"><?php echo $row['title'] ?></h2>
				</a>
			</header>
			<!-- End Card Header -->

			<!-- Card Body -->
			<div class = "card-body py-0">
				<!-- Flushed List Group -->
				<ul class = "list-group list-group-flush">

					<!-- List Group Item -->

					<!--li class = "list-group-item border-0"-->
					<div   class = "media link-dark align-items-center" href = "?deputado=<?php echo $row['id'] ?>">

						<!-- Title and Short Text -->
						
						<?php $id_topic = $row['id'];
							$sql      = "SELECT * FROM topic_term where topic = $id_topic LIMIT 5;";
							$result_2 = $conexao->query($sql);
							echo "<textarea readonly rows='11' cols='17'>";
							while ($row_term = $result_2->fetch_assoc()) {
								echo str_replace("	", "-", get_termo($conexao, $row_term['term']))?>
						<?php }?></textarea>
						
						</a>
						<!--/li-->
						<!-- End List Group Item -->


				</ul>
				<!-- End Flushed List Group -->
			</div>
			<!-- End Card Body -->
		</div>
		<!-- End Card -->
<?php }
} ?>