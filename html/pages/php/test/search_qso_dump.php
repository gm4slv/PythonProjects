 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search results</title>
    <meta http-equiv="Content-Type" content="text/html" />
</head>
 <body bgcolor="c8d5e6">
	<basefont face="Arial">
<center>


<?php
  


$coast_mmsi=$_GET['coast_mmsi'];


echo "<h3>Dump of all messages between $coast_mmsi and any ship</h3>";

//$DATEQUERY="DATE_FORMAT(DATETIME, '%Y') like '%".$year."%' and DATE_FORMAT(DATETIME, '%m') like '%".$month."%' and DATE_FORMAT(DATETIME, '%d') like '%".$day."%'";

//$DATEQUERY="datetime > date_sub(utc_timestamp(), interval 24 hour)";



$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./tmp/' . $fd . '.txt';

$f = fopen($file, 'w');

//  $output = "$datetime;$rx_id;$rx_freq;$to_type;$to_mmsi;$to_name;$to_ctry;$cat;$from_type;$from_mmsi;$from_name;$from_ctry;$tc1;$tc2;$freq;$pos;$eos;$ecc\r\n";

$header = "Datetime;rx_id;rx_freq;fmt;to_type;to_mmsi;to_name;to_ctry;cat;from_type;from_mmsi;from_name;from_ctry;tc1;tc2;freq;pos;eos;ecc\r\n\r\n";
fwrite($f, $header);



$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


$result = mysqli_query($con, " select * from newlog where TC1 not like '%test%' and  (  (RAW_TO_MMSI = ".$coast_mmsi." and FROM_TYPE='SHIP') or (TO_TYPE='SHIP' and RAW_FROM_MMSI=".$coast_mmsi.")) order by datetime desc");

//      $result = mysqli_query($con,"SELECT * FROM newlog where ".$DATEQUERY." and RX_ID like '%".$rxid."%' and (rx_freq = '$f1' or rx_freq = '$f2' or rx_freq = '$f3' or rx_freq = '$f4' or rx_freq = '$f5' or rx_freq = '$f6' or rx_freq = '$f7' or rx_freq = '$f8' or rx_freq like '%".$allf."%' ) order by datetime $order limit $limit ");

echo "File output in csv format for importing into Excel etc. <br>";      
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";     
      



while($row = mysqli_fetch_array($result))
{

  
  $datetime = $row['DATETIME'];
  $rx_freq = $row['RX_FREQ'];
  $fmt = $row['FMT'];
  $to_type = $row['TO_TYPE'];
  $to_mmsi = $row['RAW_TO_MMSI'];
  $to_name = $row['TO_NAME'];
  $to_ctry = $row['TO_CTRY'];
  $cat = $row['CAT'];
  $from_type = $row['FROM_TYPE'];
  $from_mmsi = $row['RAW_FROM_MMSI'];
  $from_name = $row['FROM_NAME'];
  $from_ctry = $row['FROM_CTRY'];
  $tc1 = $row['TC1'];
  $tc2 = $row['TC2'];
  $freq = $row['FREQ'];
  $pos = $row['POS'];
  $eos = $row['EOS'];
  $ecc = $row['ECC'];
  $rx_id = $row['RX_ID'];
  $raw_dsc_message = $row['RAW_DSC_MESSAGE']; 
  
  $output = "$datetime;$rx_id;$rx_freq;$fmt;$to_type;$to_mmsi;$to_name;$to_ctry;$cat;$from_type;$from_mmsi;$from_name;$from_ctry;$tc1;$tc2;$freq;$pos;$eos;$ecc\r\n";
  
  fwrite($f, $output);
  
  
  }
echo "</table>";
echo "</font>";


//$command='/bin/sed -i \'s/<br>/: /g\' '.str_replace(' ','\ ',$file);
//     exec($command);
//$command='/bin/sed -i \'s/<f.*n>//g\' '.str_replace(' ','\ ',$file);
//      exec($command);
//$command='/bin/sed -i \'s/<\/font>//g\' '.str_replace(' ','\ ',$file);
//      exec($command);
//$command='/bin/sed -i \'s/<a.*mmsi//g\' '.str_replace(' ','\ ',$file);
//      exec($command);
//$command='/bin/sed -i \'s/\".*>//g\' '.str_replace(' ','\ ',$file);
//      exec($command);


fclose($f);
mysqli_close($con);
?>
</center>
<center><br><a href="./search_qso_index2.php">TRY AGAIN</a></body>
</html>

