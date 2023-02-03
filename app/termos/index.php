<!DOCTYPE html>
<?php

require_once("../conexao.php");

?>
<html lang="en" class="no-js">
	<!-- Head -->
	<head>
		<title>Documentos</title>

		<!-- Meta -->
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">

    <!-- Favicon -->
    <link rel="shortcut icon" href="../favicon.png" type="image/x-icon">

    <!-- Web Fonts -->
    <link href="//fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">

		
		
		

		<!-- Theme Styles -->
		<link rel="stylesheet" href="../css/theme.css">
	</head>
	<!-- End Head -->

	<!-- Body -->
	<body>
    <!-- Header (Topbar) -->

    <?php include("../header.html"); ?>

    <!-- End Header (Topbar) -->

		<!-- Main -->
		<main class="u-main">
			<!-- Sidebar -->
			<?php include("../sidebar.html"); ?>
			<!-- End Sidebar -->

			<!-- Content -->
			<div class="u-content">
				<!-- Content Body -->
				<div class="u-body">
					<div class="row">
						<div class="">
							
							
						</div>

						<div class="row col-md-12 col-lg-12" >
							<?php include("termos.php"); ?>

						</div>
					</div>
				</div>
				<!-- End Content Body -->

				<?php include("../footer.html") ?>
			</div>
			<!-- End Content -->
		</main>
		<!-- End Main -->

		
		
		
		
		

		
		

		<!-- Initialization  -->
		
		
	</body>
	<!-- End Body -->
</html>

<?php $conexao->close(); ?>