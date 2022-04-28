 
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
$year=$_GET['year'];
$month=$_GET['month'];
$day=$_GET['day'];
$fmt=$_GET['fmt'];
$cat=$_GET['cat'];
$fp=$_GET['fp'];
$eos=$_GET['eos'];
$ecc=$_GET['ecc'];
$cecc=$_GET['cecc'];
//$rx_freq=$_GET['rx_freq'];

$mmsi=$_GET['mmsi'];
$both=$_GET['both'];
$tc1=$_GET['tc1'];
$tc2=$_GET['tc2'];
$from_mid=$_GET['from_mid'];
$to_mid=$_GET['to_mid'];
$toormid=$_GET['toormid'];
$fromormid=$_GET['fromormid'];
$limit=$_GET['limit'];
$order=$_GET['order'];
$and=$_GET['andor'];
$from_mmsi=$_GET['from_mmsi'];
$to_mmsi=$_GET['to_mmsi'];
$infile=$_GET['infile'];

$choosefreq=$_GET['choosefreq'];


$f1=$_GET['f1'];
$f2=$_GET['f2'];
$f3=$_GET['f3'];
$f4=$_GET['f4'];
$f5=$_GET['f5'];
$f6=$_GET['f6'];
$f7=$_GET['f7'];
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

if (empty($allf))
{
$allf="NULL";
}
else
{
$allf="%";
}



$DATEQUERY="DATE_FORMAT(DATETIME, '%Y') like '%".$year."%' and DATE_FORMAT(DATETIME, '%m') like '%".$month."%' and DATE_FORMAT(DATETIME, '%d') like '%".$day."%'";



if ($tc1=="notest")
{
$notest="TEST";
$tc1="";
}


if (!empty($from_type))

{ 
$from_mmsi=$from_type;
}

if (!empty($to_type))

{ 
$to_mmsi=$to_type;
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
}
else
	if ($fromormid=="mid")
	{
	//echo "using from_mid<br>";
		$from_mmsi="COAST,$from_mid";
	}

if ($both=="both")
{ 
	//echo "both checked (to)<br>";
	$to_mmsi=$mmsi;
	$and="or";
}
else
	if ($toormid=="mid")
	{
		//echo "using to_mid<br>";
		$to_mmsi="COAST,$to_mid";
	}

	
	// change to a single log table, instead of a separate ERRLOG


$log="full_log";

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


      $result = mysqli_query($con,"SELECT * FROM $log where ".$DATEQUERY." and FMT like '%".$fmt."%' and CAT like '%".$cat."%' and (rx_freq = '$f1' or rx_freq = '$f2' or rx_freq = '$f3' or rx_freq = '$f4' or rx_freq = '$f5' or rx_freq = '$f6' or rx_freq = '$f7' or rx_freq like '%".$allf."%' ) and RX_ID like '%' and (FROM_MMSI like '%".$from_mmsi."%' ".$and." TO_MMSI like '%".$to_mmsi."%') and TC1 like '%".$tc1."%' and TC1 not like '".$notest."' and TC2 like '%".$tc2."%' and ".$fp_string." and EOS like '%".$eos."%' order by datetime $order limit $limit");

echo "Text file output for copying into documents/email etc <br>";      
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";     
      
echo "<table border='0' cellpadding='5' rules='all'>
<tr>
<th> <font face=monospace color=blue size='3pt'>Date  /  UTC</font></th>
<th><font face=monospace color=#424242 size='3pt'>Freq</font></th>
<th><font face=monospace color=black size='3pt'>FMT</font></th>
<th> <font  face=monospace color=brown size='3pt'>To</font></th>
<th> <font  face=monospace color=black size='3pt'>CAT</font></th>
<th> <font  face=monospace color=DarkGreen size='3pt'>From</font></th>
<th> <font  face=monospace color=blue size='3pt'>TC1</font></th>
<th> <font  face=monospace color=blue size='3pt'>TC2</font></th>
<th> <font  face=monospace color=crimson size='3pt'>Freq</font></th>
<th> <font  face=monospace color=crimson size='3pt'>Pos</font></th>
<th> <font  face=monospace color=blue size='3pt'>EOS</font></th>
<th> <font  face=monospace color=#424242 size='2pt'>ECC</font></th>
<th><font face=monospace color=#541b66 size='3pt'>RX_ID</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";
  echo "<td width='6%' nowrap><font face=monospace color=blue size='3pt'>"  . $row['DATETIME'] . "</font> </td>";
  echo "<td width='4%'><font  face=monospace color=#424242 size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
  echo "<td width='2%'><font  face=monospace color=black size='3pt'>" . $row['FMT'] . "</font></td>";
  echo "<td width='22%'><font face=monospace color=black size='3pt'>" . $row['TO_MMSI'] . "</font></td>";
  echo "<td width='2%'><font  face=monospace color=black size='3pt'>" . $row['CAT'] . "</font></td>";
  echo "<td width='22%'><font  face=monospace color=black size='3pt'>" . $row['FROM_MMSI'] . "</font></td>";
  echo "<td width='5%'><font  face=monospace color=blue size='3pt'>" . $row['TC1'] . "</font></td>";
  echo "<td width='5%'><font  face=monospace color=blue size='3pt'>" . $row['TC2'] . "</font></td>";
  echo "<td width='11%'><font  face=monospace color=crimson size='3pt'>" . $row['FREQ'] . "</font></td>";
  echo "<td width='6%'><font  face=monospace color=crimson size='3pt'>" . $row['POS'] . "</font></td>";
  echo "<td width='2%'><font  face=monospace color=blue size='3pt'>" . $row['EOS'] . "</font></td>";
  echo "<td><font  face=monospace color=#424242 size='2pt'>" . $row['ECC'] . "</font></td>";
  echo "<td width='8%' nowrap><font  face=monospace color=#541b66 size='3pt'>" . $row['RX_ID'] . "</font></td>";
  echo "</tr>";
  
  $datetime = $row['DATETIME'];
  $rx_freq = $row['RX_FREQ'];
  $fmt = $row['FMT'];
  $to_mmsi = $row['TO_MMSI'];
  $cat = $row['CAT'];
  $from_mmsi = $row['FROM_MMSI'];
  $tc1 = $row['TC1'];
  $tc2 = $row['TC2'];
  $freq = $row['FREQ'];
  $pos = $row['POS'];
  $eos = $row['EOS'];
  $ecc = $row['ECC'];
  $rx_id = $row['RX_ID'];
  
  
  $output = "     Time :\t$datetime\r\n  Monitor :\t$rx_id\r\nFrequency :\t$rx_freq kHz\r\n   Format :\t$fmt\r\n       To :\t$to_mmsi\r\n Category :\t$cat\r\n     From :\t$from_mmsi\r\n   Tele 1 :\t$tc1\r\n   Tele 2 :\t$tc2\r\n     Freq :\t$freq\r\n      Pos :\t$pos\r\n      EOS :\t$eos\r\n      ECC :\t$ecc\r\n\r\n\r\n";
  //$output = "$datetime;$rx_id;$rx_freq;$fmt;$to_mmsi;$cat;$from_mmsi;$tc1;$tc2;$eos;$ecc\r\n";
  fwrite($f, $output);
  }
echo "</table>";
echo "</font>";
echo "</center><br><br>";
//echo "<font  face=monospace color=#424242 size='3pt'>================ Search Terms Used ================<br><br>Date: '".$year."'-'".$month."'-'".$day."'<br><br>  RX1: '".$rx1."'  RX2: '".$rx2."'  RX3: '".$rx3."'<br><br>Freq: '".$rx_freq."' Format: '".$fmt."' Category: '".$cat."' TC1: '".$tc1."' / NOT '".$notest."'<br><br>To MMSI: '".$to_mmsi."' '".$and."' From MMSI: '".$from_mmsi."' ECC: '".$ecc."' Sort Order: '".$order."' Results Range: '".$limit."'<br><br></font>";

//echo "<font  face=monospace color=#424242 size='3pt'>==================== SQL Query ====================<br><br>'SELECT * FROM log where  DATE_FORMAT(DATETIME, '%Y') like '%".$year."%' and DATE_FORMAT(DATETIME, '%m') like '%".$month."%' and DATE_FORMAT(DATETIME, '%d') like '%".$day."%' and FMT like '%".$fmt."%' and CAT like '%".$cat."%' and ECC like '%".$ecc."%' and RX_FREQ like '%".$rx_freq."%' and (RX_ID like '%".$rx1."%' or RX_ID like '%".$rx2."%' or RX_ID like '%".$rx3."%') and (FROM_MMSI like '%".$from_mmsi."%' ".$and." TO_MMSI like '%".$to_mmsi."%') and TC1 like '%".$tc1."%' and TC1 not like '".$notest."' order by datetime $order limit $limit'<br><br><br><br></font>";



	  

$command='/bin/sed -i \'s/,/ /g\' '.str_replace(' ','\ ',$file);
      exec($command);
$command='/bin/sed -i \'s/<br>/ : /g\' '.str_replace(' ','\ ',$file);
      exec($command);
$command='/bin/sed -i \'s/<font color=green>//g\' '.str_replace(' ','\ ',$file);
      exec($command);
$command='/bin/sed -i \'s/<font color=brown>//g\' '.str_replace(' ','\ ',$file);
      exec($command);
$command='/bin/sed -i \'s/</font>//g\' '.str_replace(' ','\ ',$file);
    exec($command);
$command='/bin/sed -i \'s/<\/font>//g\' '.str_replace(' ','\ ',$file);
    exec($command);
$command='/bin/sed -i \'s/<a.*mmsi//g\' '.str_replace(' ','\ ',$file);
      exec($command);
$command='/bin/sed -i \'s/\".*>//g\' '.str_replace(' ','\ ',$file);
      exec($command);


      fclose($f);
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br>";
#echo "<br>Preview....<br>";
#echo "<iframe width=60% height=800 src=".$file."></iframe>";


mysqli_close($con);
?>

</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>
 
