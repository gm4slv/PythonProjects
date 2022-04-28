 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Dubious Goals Panel</title>
<meta http-equiv="refresh" content="120">
<meta http-equiv="Content-Type" content="text/html" />
</head>
 <body bgcolor="c8d5e6">
	<basefont face="Arial">

<font face=monospace size='3pt'>

<h3>Looking for <i>dubious</i> database records</h3>
These records may be due to incorrect setting of YaDD's frequency, but<i> also may be due to operator error, or faults, at the Coast Station itself.</i><br><br>
The choice of search criteria is intended to show that <i>something is wrong</i> with the database. Finding the full extent (and correcting it where necessary)
is a lengthy, manual, process though. Please help by ensuring your YaDD settings match the actual RX frequency. Be especially careful when changing frequency to keep
YaDD and RX in sync!<br>
<br>
If I notice a contributor with an obvious reporting error I will try and correct it, and <i>might</i> set up automatic correction to run every 10 minutes to change the reported
frequency of their incoming data until they change their YaDD or RX frequency. My goal is to have the data in YaDDNet be as accurate as possible!
<br>
<br>
<hr>
Be within the last 7 days
<hr>
<b>AND</b>
<hr>
(rx_freq <b>greater than</b> 2187.5 and from_type = coast and (from_mid = 244 or 261 or 232 or 250 or 211 or from_mmsi=002191000 or 002241024) and not from snargate)
<br>
<br>
<b>OR</b>
<br>
<br>
(rx_freq <b>equals</b> 2187.5 and from_type = coast and (from_mid = 366 or 503))
<br>
<br>
<b>OR</b>
<br>
<br>
(rx_freq not (8414.5 or 12577.0) and from_mmsi = 003660003)
<br>
<hr>
The first test checks for erroneous reporting of an HF frequency when RX is really on 2187.5
<br><br>MID 244 = Netherlands, MID 261 = Poland (Witowo mainly), MID 232 = UK (Coastguard), MID 250 = Eire, MID 211 = Germany, MMSI=002191000 (Lyngby), MMSI=002241024 (Valencia).
<br><br><b>None of these Coast Station MIDs are active on HF</b><br>
Apart from the <i>"Snargate MID=232 and MMSI 002320204"</i><br>
<br>
<hr>
The second test checks for erroneous reporting of 2187.5 when the RX is really on an HF frequency<br>
<br>MID 366 = USA, MID 503 = Australia<br>
<br><b>Neither of these Coast Station MIDs is active on 2MHz</b><br>
<br>
<hr>
The third test checks for erroneous HF band selection - <b>WLO 003660003</b> only operates on 8MHz and 12MHz. Any spots of them on other bands indicates a problem
<br>
<hr>
</font>
<center>
<?php
  

$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./tmp/' . $fd . '.txt';

$f = fopen($file, 'w');


$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }



	$result = mysqli_query($con, "select * from newlog where DATETIME>date_sub(now(), interval 7 day) and (RX_FREQ > '2187.5' and FROM_TYPE = 'COAST' and ( FROM_MID = 244 or RAW_FROM_MMSI = '002191000' or FROM_MID = 261 or FROM_MID = 232 or FROM_MID = 250 or FROM_MID = 211 or RAW_FROM_MMSI='002241024') and RAW_FROM_MMSI != '002320204'  and RAW_FROM_MMSI != '219015591' ) or (RX_FREQ = '2187.5' and FROM_TYPE = 'COAST' and (FROM_MID = 366 or FROM_MID = 503)) or (RX_FREQ != '8414.5' and RX_FREQ != '12577.0' and RAW_FROM_MMSI = '003660003' ) order by DATETIME desc");








// CUT HERE.....


// A TEST

echo "<br>";

echo "<h3>Results</h3>";
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

  echo "<td width='6%'><font face=monospace color=blue size='3pt'><a href='../search_qso.php?coast_mmsi=" . $row['RAW_TO_MMSI']. "&ship_mmsi=". $row['RAW_FROM_MMSI']."' >" . $row['DATETIME'] . "</a></font> </td>";
//  echo "<td width='6%'><font face=monospace color=blue size='3pt'>"  . $row['DATETIME'] . "</font> </td>";
  echo "<td width='4%'><font  face=monospace color=#424242 size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
  echo "<td align=center width='2%'><font  face=monospace color=black size='3pt'>" . $row['FMT'] . "</font></td>";


  echo "<td  width='22%' nowrap><font face=monospace color=$colorto size='3pt'>" . $row['TO_TYPE'] . "<br></font>";

if ($row['TO_TYPE'] == "AREA")
  echo " <font face=monospace color=$colorto size='3pt'>" . $row['RAW_TO_MMSI'] . "</font><br>";
else


echo " <font face=monospace color=$colorto size='3pt'><a href='../band_today_messages.php?from_mmsi=" . $row['RAW_TO_MMSI'] . "&rx_freq=" . $row['RX_FREQ'] . "' style='color:$colorto' >" . $row['RAW_TO_MMSI'] . "</a></font><br>";
  

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
echo " <font face=monospace color=$colorfrom size='3pt'><a href='../band_today_messages.php?from_mmsi=" . $row['RAW_FROM_MMSI'] . "&rx_freq=" . $row['RX_FREQ'] ."' style='color:$colorfrom' >" . $row['RAW_FROM_MMSI'] . "</a></font><br>";
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
echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='../search_rx_freq.php?rxid=" . $row['RX_ID'] . "&rx_freq=" . $row['RX_FREQ']."' style='color:#541B66' >" . $row['RX_ID'] . "</a></font></td>"; 

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
echo "<hr>";
echo "<a href=".$file.">File output</a><br><br>";

echo "</font>";














fclose($f);
mysqli_close($con);
?>
</center>
<center><br><a href="../../../index.php">HOME</a></body>
</html>

