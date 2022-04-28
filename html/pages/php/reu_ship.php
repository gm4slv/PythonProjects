 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Report</title>
    <meta http-equiv="Content-Type" content="text/html" />
</head>
 <body bgcolor="c8d5e6">
	<basefont face="Arial">
<center>

<?php

$rx=$_GET['rxid'];

$unid=$_GET['unid'];

$p=$_GET['p'];

if ($p<"8")
{
$pp=$p-1;
}
else
{
$pp=0;
}
//$showrx="yes";
$showrx=$_GET['showrx'];
//$eccc=$_GET['eccc'];
$eccc="ok";

// Frequency ONE ///////////////////////////////

$rx_freq="2177.0";
$i = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');
//$head="Receivers used for collation:   " . $rx1 . " / " . $rx2 . " / " . $rx3 . " / " . $rx4 . "\n\n";
$header="YYYYMMDD HHMM  kHz   MMSI       Station ID, Country\n==========================================================\n";


fwrite($f, $header);


$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];
$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	

fwrite($f, $output);
$i++;
}


mysqli_close($con);

// Frequency TWO ///////////////////////////////

$rx_freq="2187.5";
$j = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 



$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];
$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	

fwrite($f, $output);
$j = $j + 1;
}


mysqli_close($con);

// Frequency THREE ///////////////////////////////

$rx_freq="4207.5";
$k = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(FROM_MMSI), ECC from log where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and from_mmsi REGEXP 'COAST[[.space.]]' and from_mmsi not like '%~%' and from_mmsi not like '%".$unid."%' and ecc like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by from_mmsi order by from_mmsi"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];

$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	


fwrite($f, $output);
$k++;
}


mysqli_close($con);

// Frequency FOUR ///////////////////////////////

$rx_freq="6312.0";
$l = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='COAST' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(FROM_MMSI), ECC from log where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and from_mmsi REGEXP 'COAST[[.space.]]' and from_mmsi not like '%~%' and from_mmsi not like '%".$unid."%' and ecc like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by from_mmsi order by from_mmsi"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];

$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	

fwrite($f, $output);
$l++;
}


mysqli_close($con);

// Frequency FIVE ///////////////////////////////

$rx_freq="8414.5";
$m = 0;
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='COAST' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(FROM_MMSI), ECC from log where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and from_mmsi REGEXP 'COAST[[.space.]]' and from_mmsi not like '%~%' and from_mmsi not like '%".$unid."%' and ecc like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by from_mmsi order by from_mmsi"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ecc = $row['ECC'];
$ctry = $row['FROM_CTRY'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	


fwrite($f, $output);
$m++;
}


mysqli_close($con);

// Frequency SIX ///////////////////////////////

$rx_freq="12577.0";
$n = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='COAST' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(FROM_MMSI), ECC from log where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and from_mmsi REGEXP 'COAST[[.space.]]' and from_mmsi not like '%~%' and from_mmsi not like '%".$unid."%' and ecc like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by from_mmsi order by from_mmsi"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];

$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	

fwrite($f, $output);
$n++;
}


mysqli_close($con);

// Frequency SEVEN ///////////////////////////////

$rx_freq="16804.5";
$o = 0;

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='COAST' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 

$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_NAME, FROM_CTRY, ECC from newlog where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and FROM_TYPE='SHIP' and RAW_FROM_MMSI not like '%~%' and FROM_NAME not like '%".$unid."%' and ECC like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by RAW_FROM_MMSI order by RAW_FROM_MMSI"); 


//$result = mysqli_query($con,"select DATE_FORMAT(DATETIME, '%Y%m%d %H%i'), RX_FREQ, RX_ID, MIN(FROM_MMSI), ECC from log where (datetime>date_sub(curdate(), interval $p day) and datetime<date_sub(curdate(), interval $pp day)) and rx_freq like '%".$rx_freq."%' and from_mmsi REGEXP 'COAST[[.space.]]' and from_mmsi not like '%~%' and from_mmsi not like '%".$unid."%' and ecc like '%".$eccc."%' and RX_ID like '%".$rx."%'  group by from_mmsi order by from_mmsi"); 

$marker = "\n$rx_freq :\n";
fwrite($f, $marker);

while ($row=mysqli_fetch_array($result)) {

$datetime = $row['DATE_FORMAT(DATETIME, \'%Y%m%d %H%i\')'];
$rx_freq = $row['RX_FREQ'];
$rx_id = $row['RX_ID'];
//$rx_id="[YaDDNet]";
$from_mmsi = $row['MIN(RAW_FROM_MMSI)'];
$from_name = $row['FROM_NAME'];
$ctry = $row['FROM_CTRY'];
$ecc = $row['ECC'];

if ($showrx=="yes")
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\t\t\t$rx_id\n";
}
else
{
	$output = "$datetime $rx_freq $from_mmsi $from_name, $ctry\n";
}	

fwrite($f, $output);
$o++;

}
$foot="\n\nTotal 2177.0kHz : " . $i . "\nTotal 2187.5kHz : " . $j . "\nTotal 4207.5kHz : " . $k . "\nTotal 6312.0kHz : " . $l . "\nTotal 8414.5kHz : " . $m . "\nTotal 12577.0kHz : " . $n . "\nTotal 16804.5kHz : " . $o . "\n";
fwrite($f, $foot);

fclose($f);

mysqli_close($con);


// Remove "COAST" from each record

echo "<br><br>";
//echo "Receivers used : " . $rx1 . " " . $rx2 . " " .$rx3. " " .$rx4. "<br><br>";
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br>";
echo "<br>Preview....<br>";
echo "<iframe width=60% height=800 src=".$file."></iframe>";

//mysqli_close($con);
?>
<br><br><br>
<a href="../../index.php">HOME</a>
</center>
</body>
</html>
 
