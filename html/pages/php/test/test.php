 
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
  


$year=$_GET['year'];
$month=$_GET['month'];
$day=$_GET['day'];

$rxid=$_GET['rxid'];

$fmt=$_GET['fmt'];
$cat=$_GET['cat'];
$tc1=$_GET['tc1'];

if (empty($fmt))
{
$fmt="%";
}

if (empty($cat))
{
$cat="%";
}
if (empty($tc1))
{
$tc1="%";
}

echo "<h3>Showing last 24 hours messages from <i> ".$rxid."</i> on all frequencies.</h3>";

//$DATEQUERY="DATE_FORMAT(DATETIME, '%Y') like '%".$year."%' and DATE_FORMAT(DATETIME, '%m') like '%".$month."%' and DATE_FORMAT(DATETIME, '%d') like '%".$day."%'";

$DATEQUERY="datetime > date_sub(utc_timestamp(), interval 24 hour)";



$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');



$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


      $result = mysqli_query($con,"SELECT * FROM newlog where ".$DATEQUERY." and (FMT like '%".$fmt."%' and CAT like '%".$cat."%' and TC1 like '%".$tc1."%') order by datetime desc limit 25");










// CUT HERE.....


// A TEST

echo "<br>";
echo "Text file output for copying into documents/email etc <br>";      
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";


echo "<table border='0' cellpadding='5' rules='all'>
<tr>
<th> <font face=monospace color=blue size='3pt'>Date  /  UTC</font></th>
<th><font face=monospace color=#424242 size='3pt'>Freq</font></th>
<th><font face=monospace color=black size='3pt'>FMT</font></th>
<th> <font  face=monospace color=black size='3pt'>To</font></th>
<th> <font  face=monospace color=black size='3pt'>CAT</font></th>
<th> <font  face=monospace color=black size='3pt'>From</font></th>
<th> <font  face=monospace color=blue size='3pt'>TC1</font></th>
<th> <font  face=monospace color=blue size='3pt'>TC2</font></th>
<th> <font  face=monospace color=crimson size='3pt'>Freq</font></th>
<th> <font  face=monospace color=crimson size='3pt'>Pos</font></th>
<th> <font  face=monospace color=blue size='3pt'>EOS</font></th>
<th> <font  face=monospace color=#424242 size='3pt'>ECC</font></th>
<th><font face=monospace color=#541b66 size='3pt'>RX_ID</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
{

	if ($row['TO_TYPE'] == "SHIP")
		$colorto = "brown";
	else if ($row['TO_TYPE'] == "COAST")
		$colorto = "green";
	else if ($row['TO_TYPE'] == "GROUP")
		$colorto = "blue";
	else
		$colorto = "black";


	if ($row['FROM_TYPE'] == "SHIP")
		$colorfrom = "brown";
	else if ($row['FROM_TYPE'] == "COAST")
		$colorfrom = "green";
	else if ($row['FROM_TYPE'] == "GROUP")
		$colorfrom = "blue";
	else
		$colorfrom = "black";


  echo "<tr>";

  echo "<td width='6%'><font face=monospace color=blue size='3pt'><a href='./search_qso.php?coast_mmsi=" . $row['RAW_TO_MMSI']. "&ship_mmsi=". $row['RAW_FROM_MMSI']."' >" . $row['DATETIME'] . "</a></font> </td>";
//  echo "<td width='6%'><font face=monospace color=blue size='3pt'>"  . $row['DATETIME'] . "</font> </td>";
  echo "<td width='4%'><font  face=monospace color=#424242 size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
  echo "<td align=center width='2%'><font  face=monospace color=black size='3pt'>" . $row['FMT'] . "</font></td>";


  echo "<td  width='22%' nowrap><font face=monospace color=$colorto size='3pt'>" . $row['TO_TYPE'] . "<br></font>";

if ($row['TO_TYPE'] == "AREA")
  echo " <font face=monospace color=$colorto size='3pt'>" . $row['RAW_TO_MMSI'] . "</font><br>";
else


echo " <font face=monospace color=$colorto size='3pt'><a href='./band_today_messages.php?from_mmsi=" . $row['RAW_TO_MMSI'] . "&rx_freq=" . $row['RX_FREQ'] . "' style='color:$colorto' >" . $row['RAW_TO_MMSI'] . "</a></font><br>";
  

//	  echo " <font face=monospace color=$colorto size='3pt'>" . $row['RAW_TO_MMSI'] . " </font><br>";
  
if ($row['TO_TYPE'] == "SHIP")
	  echo "<font face=monospace color=black size='3pt'><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:". $row['RAW_TO_MMSI']."\">".$row['TO_NAME']."</a></font><br><font face=monospace color=black size='3pt'>" . $row['TO_CTRY'] . "</font></td>";
 else if ($row['TO_TYPE'] == "COAST")
	  echo "<font face=monospace color=black size='3pt'>" . $row['TO_NAME'] . "</font><br><font face = monospace color=black size='3pt'>" . $row['TO_CTRY']. "</font></td>";
  else if ($row['TO_TYPE'] == "GROUP")

	 echo "<font  face=monospace color=black size='3pt'>" . $row['TO_NAME'] . "</font><br><font face=monospace color=black size='3pt'>" . $row['TO_CTRY'] . "</font></td>";
else if ($row['TO_TYPE'] == "ALL")
        echo "<font  face=monospace color=black size='3pt'>" . $row['TO_NAME'] . "</font></td>";  
  
  echo "<td align=center width='2%'><font  face=monospace color=black size='3pt'>" . $row['CAT'] . "</font></td>";

  echo "<td  width='22%' nowrap><font face=monospace color=$colorfrom size='3pt'>" . $row['FROM_TYPE'] . "<br></font>";
echo " <font face=monospace color=$colorfrom size='3pt'><a href='./band_today_messages.php?from_mmsi=" . $row['RAW_FROM_MMSI'] . "&rx_freq=" . $row['RX_FREQ'] ."' style='color:$colorfrom' >" . $row['RAW_FROM_MMSI'] . "</a></font><br>";
//  echo " <font face=monospace color=$colorfrom size='3pt'>" . $row['RAW_FROM_MMSI'] . " </font><br>";
  if ($row['FROM_TYPE'] == "SHIP")
	  echo "<font face=monospace color=black size='3pt'><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:". $row['RAW_FROM_MMSI']."\">".$row['FROM_NAME']."</a></font><br><font face=monospace color=black size='3pt'>" . $row['FROM_CTRY'] . "</font></td>";
  else if ($row['FROM_TYPE'] == "COAST")
	  echo "<font face=monospace color=black size='3pt'>" . $row['FROM_NAME'] . "</font><br><font face = monospace color=black size='3pt'>" . $row['FROM_CTRY']. "</font></td>";
  else if ($row['FROM_TYPE'] == "GROUP")
	 echo "<font  face=monospace color=black size='3pt'>" . $row['FROM_NAME'] . "</font><br><font face=monospace color=black size='3pt'>" . $row['FROM_CTRY'] . "</font></td>";
  


  echo "<td width='5%'><font  face=monospace color=blue size='3pt'>" . $row['TC1'] . "<font></td>";
  echo "<td width='5%'><font  face=monospace color=blue size='3pt'>" . $row['TC2'] . "<font></td>";
  echo "<td width='11%'><font  face=monospace color=crimson size='3pt'>" . $row['FREQ'] . "<font></td>";
  echo "<td width='6%'><font  face=monospace color=crimson size='3pt'>" . $row['POS'] . "<font></td>";
  echo "<td align=center width='2%'><font  face=monospace color=blue size='3pt'>" . $row['EOS'] . "<font></td>";
  echo "<td align=center width='5%'><font face=monospace color=#424242 size='3pt'>" . $row['ECC'] . "<font></td>";
echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['RX_ID'] . "&rx_freq=" . $row['RX_FREQ']."' style='color:#541B66' >" . $row['RX_ID'] . "</a></font></td>"; 

// echo "<td width='8%' ><font  face=monospace color=#541b66 size='3pt'>" . $row['RX_ID'] . "</font></td>";
  echo "</tr>";
  
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

   $output = "    Input :\t$raw_dsc_message\r\n     Time :\t$datetime\r\n  Monitor :\t$rx_id\r\nFrequency :\t$rx_freq kHz\r\n   Format :\t$fmt\r\n       To :\t$to_type\t$to_mmsi : $to_name : $to_ctry\r\n Category :\t$cat\r\n     From :\t$from_type\t$from_mmsi : $from_name : $from_ctry\r\n   Tele 1 :\t$tc1\r\n   Tele 2 :\t$tc2\r\n     Freq :\t$freq\r\n      Pos :\t$pos\r\n      EOS :\t$eos\r\n      ECC :\t$ecc\r\n\r\n"; 
  
  
  fwrite($f, $output);
  
  
  }
echo "</table>";
echo "</font>";



fclose($f);
mysqli_close($con);
?>
</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

