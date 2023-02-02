<!DOCTYPE html>
<?php

require_once("conexao.php");

?>
<html lang="en" class="no-js">
	<!-- Head -->
	<head>
		<title>TCC - Modelo de Tópicos</title>

		<!-- Meta -->
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">

    <!-- Favicon -->
    <link rel="shortcut icon" href="favicon.png" type="image/x-icon">

    <!-- Web Fonts -->
    <link href="//fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
		<!-- Theme Styles -->
		<link rel="stylesheet" href="css/theme.css">
	</head>
	<!-- End Head -->

	<!-- Body -->
	<body>
    <!-- Header (Topbar) -->

    <?php include("header.html"); ?>

    <!-- End Header (Topbar) -->

		<!-- Main -->
		<main class="u-main">
			<!-- Sidebar -->
			<?php include("sidebar.html"); ?>
			<!-- End Sidebar -->

			<!-- Content -->
			<div class="u-content">
				<!-- Content Body -->
				<div class="u-body">
					<div class="row">
						<div class="col-md-5 col-lg-4">
							<!-- Card Político Figura-->
							<?php include("topics.php"); ?>
							<!-- End Card -->
							<!-- Card Político Figura-->
							<?php include("termos.php"); ?>
							<!-- End Card -->
							
						</div>

						<div class="col-md-7 col-lg-8">
							<?php include("docs.php"); ?>

						</div>
					</div>
				</div>
				<!-- End Content Body -->

				<?php include("footer.html") ?>
			</div>
			<!-- End Content -->
		</main>
		<!-- End Main -->

		<!-- Global Vendor -->
		<script src="assets/vendor/jquery/dist/jquery.min.js"></script>
		<script src="assets/vendor/jquery-migrate/jquery-migrate.min.js"></script>
		<script src="assets/vendor/popper.js/dist/umd/popper.min.js"></script>
		<script src="assets/vendor/bootstrap/dist/js/bootstrap.min.js"></script>

		<!-- Plugins -->
		<script src="assets/vendor/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.concat.min.js"></script>

		<!-- Initialization  -->
		<script src="assets/js/sidebar-nav.js"></script>
		<script src="assets/js/main.js"></script>
	</body>
	<!-- End Body -->
</html>

<?php $conexao->close(); ?>