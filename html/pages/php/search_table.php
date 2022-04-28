 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search results</title>
    <meta http-equiv="Content-Type" content="text/html" />
</head>
 <body bgcolor="c8d5e6">
	<basefont face="Arial">
<center>

<h3>Search Results</h3>

<?php
  


$from_type=$_GET['fromtype'];
$to_type=$_GET['totype'];
$to_mid=$_GET['to_mid'];
$from_mid=$_GET['from_mid'];

$to_mid_type=$_GET['tomidtype'];
$from_mid_type=$_GET['frommidtype'];

$year=$_GET['year'];
$month=$_GET['month'];
$day=$_GET['day'];
$fmt=$_GET['fmt'];
$cat=$_GET['cat'];
$fp=$_GET['fp'];
$eos=$_GET['eos'];
//$ecc=$_GET['ecc'];
$cecc=$_GET['cecc'];
//$rx_freq=$_GET['rx_freq'];

//$allr=$_GET['selectallr'];
$allr="True";


$mmsi=$_GET['mmsi'];
$both=$_GET['both'];
$tc1=$_GET['tc1'];
$tc2=$_GET['tc2'];
//$from_mid=$_GET['from_mid'];
//$to_mid=$_GET['to_mid'];
//$toormid=$_GET['toormid'];
//$fromormid=$_GET['fromormid'];
$limit=$_GET['limit'];
$order=$_GET['order'];
$and=$_GET['andor'];
$from_mmsi=$_GET['from_mmsi'];
$to_mmsi=$_GET['to_mmsi'];
$infile=$_GET['infile'];
$today=$_GET['today'];

$p=$_GET['today'];
$choosefreq=$_GET['choosefreq'];


$f1=$_GET['f1'];
$f2=$_GET['f2'];
$f3=$_GET['f3'];
$f4=$_GET['f4'];
$f5=$_GET['f5'];
$f6=$_GET['f6'];
$f7=$_GET['f7'];
$f8=$_GET['f8'];
$allf=$_GET['selectallf'];

if (empty($f1))
{
$f1="NULL";
}

if (empty($f2))
{
$f2="NULL";
}
if (empty($f3))
{
$f3="NULL";
}
if (empty($f4))
{
$f4="NULL";
}
if (empty($f5))
{
$f5="NULL";
}

if (empty($f6))
{
$f6="NULL";
}
if (empty($f7))
{
$f7="NULL";
}

if (empty($f8))
{
$f8="NULL";
}

if (empty($allf))
{
$allf="NULL";
}
else
{
$allf="%";
}




if ($to_type == "MID")
	{
	if ($to_mid_type == "SHIP") 
		{
		$to_type = "SHIP";
		}
	elseif ($to_mid_type == "COAST") 
		{
		$to_type = "COAST";
		}
}
else 
{
$to_mid = "%";
}




if ($from_type == "MID")
	{
	if ($from_mid_type == "SHIP") 
		{
		$from_type = "SHIP";
		}
	elseif ($from_mid_type == "COAST") 
		{
		$from_type = "COAST";
		}
}
else
{
$from_mid = "%";
}


//echo "from type ";
//echo $from_type;
//echo "<br>";
//echo "to  type";
//echo $to_type;
//echo "<br>";
//echo "to mid ";
//echo $to_mid;
//echo "<br>";
//echo "from mid ";
//echo $from_mid;
//echo "<br>";



$allr="%";

if (empty ($p))
{
$DATEQUERY="DATE_FORMAT(DATETIME, '%Y') like '%".$year."%' and DATE_FORMAT(DATETIME, '%m') like '%".$month."%' and DATE_FORMAT(DATETIME, '%d') like '%".$day."%'";
}
else 
{
$DATEQUERY="datetime>date_sub(utc_timestamp(), interval '$p' hour)";

}


if ($tc1=="notest")
{
$notest="TEST";
$tc1="";
}


if (!empty($from_type))

{ 
$from_mmsi="%";
}

if (!empty($to_type))

{ 
$to_mmsi="%";
}

if (empty($and))
{$and="and";
}


// sort out which parts are used for the MMISs

if ($both=="both")
{ 
	//echo "both checked (from)<br>";
	$from_mmsi=$mmsi;
	$and="or";
	$from_type="%";
	$from_mid = "%";
}
//else
//	if ($to_type=="COAST_MID")
//	{
	//echo "using from_mid<br>";
//		$to_type="COAST";
//		$from_mmsi="%";
##		$from_mid_min=$from_mid;
//		$from_mid_max=$from_mid+99;
//		
//	}
//	elseif ($to_type=="SHIP_MID")
//	{
//		$to_type = "SHIP";
//		$from_mmsi="%";
//		$from_mid_min=0;
//		$from_mid_max=900;
//	}

	


if ($both=="both")
{ 
	//echo "both checked (to)<br>";
	$to_mmsi=$mmsi;
	$and="or";
	$to_type="%";
	$to_mid = "%";
}
//else
//	if ($toormid=="mid")
//	{
//		//echo "using to_mid<br>";
//		$to_mmsi="%";
//		$to_mid_min=$to_mid;
//		$to_mid_min=$to_mid+99;
//
//	}
//	else 
//		$to_mid_min=0;
//		$to_mid_max=900;

	
	// change to a single log table, instead of a separate ERRLOG
if ($cecc=="ok")
{
$log="newlog";
$ecc="ok";
}
elseif ($cecc=="err")
{
$log="newlog";
$ecc="err";
}
else 
{
$log="newlog";
$ecc="";
}

if ($fp=="fq")
{
$fp_string=" freq not like '%--%' ";
}
elseif ($fp=="pos")
{
$fp_string=" pos not like '%--%' ";
}
else 
{
$fp_string=" freq like '%' and pos like '%' ";
}

if ($pos=="pos")
{
$pos_string=" pos not like '%--%' ";
}
elseif ($pos=="nopos")
{
$pos_string=" pos like '%--%' ";
}
else
{
$pos_string=" pos like '%' ";
}


//echo "from_mmsi    :";
//echo $from_mmsi;
//echo "<br>";
//echo "to_mmsi    :";
//echo $to_mmsi;
//echo "<br>";
//echo "from_mid    :";
//echo $from_mid;
//echo $from_mid_min;
//echo $from_mid_max;
//echo "<br>";
//echo "to_mid    :";
//echo $to_mid;
//echo "<br>";
//echo "both    :";
//echo $both;
//echo "<br>";
//echo "fromormid    :";
//echo $fromormid;
//echo "<br>";
//echo "toormid    :";
//echo $toormid;
//echo "<br>";
//echo "and   ";
//echo $and;
//echo "<br>";


$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');



$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


      $result = mysqli_query($con,"SELECT * FROM $log where ".$DATEQUERY." and FROM_TYPE like '%".$from_type."%' and TO_MID like '%".$to_mid."%' and FROM_MID like '%".$from_mid."%' and TO_TYPE like '%".$to_type."%' and FMT like '%".$fmt."%' and CAT like '%".$cat."%' and ECC like '%".$ecc."%' and (rx_freq = '$f1' or rx_freq = '$f2' or rx_freq = '$f3' or rx_freq = '$f4' or rx_freq = '$f5' or rx_freq = '$f6' or rx_freq = '$f7' or rx_freq = '$f8' or rx_freq like '%".$allf."%' ) and  RX_ID like '%".$allr."%' and ((RAW_FROM_MMSI like '%".$from_mmsi."%' or FROM_NAME like '%".$from_mmsi."%') ".$and." (RAW_TO_MMSI like '%".$to_mmsi."%' or TO_NAME like '%".$to_mmsi."%')) and TC1 like '%".$tc1."%' and TC1 not like '".$notest."' and TC2 like '%".$tc2."%' and ".$fp_string." and EOS like '%".$eos."%' order by datetime $order limit $limit");

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


//  echo " <font face=monospace color=$colorto size='3pt'>" . $row['RAW_TO_MMSI'] . " </font><br>";
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

echo "<td nowrap ><font face=monospace size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['RX_ID'] . "&rx_freq=" . $row['RX_FREQ']."' style='color:#541B66' >" . $row['RX_ID'] . "</a></font></td>";
//  echo "<td width='8%' ><font  face=monospace color=#541b66 size='3pt'>" . $row['RX_ID'] . "</font></td>";
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

