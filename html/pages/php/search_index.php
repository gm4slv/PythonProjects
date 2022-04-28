<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search</title>
    <meta http-equiv="Content-Type" content="text/html" />
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script language="javascript">

function selectallCHBoxr(){ 

if($('#selectallr').attr('checked')){
var inputs = document.getElementsByClassName('rxid');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =true; 
 } }
}
else {
var inputs = document.getElementsByClassName('rxid');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}

}

function manualr() {
var inputs = document.getElementsByName('selectallr');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}


function selectallCHBoxf(){ 

if($('#selectallf').attr('checked')){
var inputs = document.getElementsByClassName('freq');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =true; 
 } }
}
else {
var inputs = document.getElementsByClassName('freq');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}

}

function manualf() {
var inputs = document.getElementsByName('selectallf');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}




</script>
<style>

 #freq{
color: #424242;
background: #006666;
width:60px;
height:30px;
border-radius: 10px
}
 #rx {
color: #424242;
background: #6666cc;
width:140px;
height:30px;
border-radius: 10px
}
#link {
color: #424242;
background: #6699cc;
width:140px;
height:30px;
border-radius: 10px;
font-weight: bold;
}
#dis {
color: #b0b0b0;
background: #d0d0d0;
width:140px;
height:30px;
border-radius: 10px
}
input[type=submit]{
color: #424242;
background: #003366;
width:60px;
height:30px;
border-radius: 10px
font-weight: bold;
}
select {
color: #424242;
background: #6699cc;
border-radius: 10px;
height: 30px;

font-weight: bold;
}
input[type=text]{
color: #424242;
background: #cccccc;
width:140px;
height:30px;
border-radius: 10px;
border-width: 1px;
font-family: monospace;
font-size: 15px;
font-weight: bold;
padding-left: 10px;
}

 

</style>
</head>
<body bgcolor="c8d5e6">
        <basefont face="Arial">
<center>
<h3>DSC Message search</h3>
<b>Default selections shown in <font color=#424242>grey</font></b>
<hr width=50%>
<!--<font color=#424242>This search uses the <i>shorter</i> database of the previous 90 days.<br>
To search the full database (slow) look <a href="./search_full.php">here</a></font>-->
    <form action="./search_table.php" method="GET">
<table cellpadding="5">


<tr>
<td>
<input type="radio" name="today" value="2160" />Last 90 days<br>
<input type="radio" name="today" value="720" />Last 30 days<br>
<input type="radio" name="today" value="168" checked /><font color=#424242>Last 7 days</font><br>
<input type="radio" name="today" value="24" />Last 24 hours<br>
<input type="radio" name="today" value="12" />Last 12 hours<br>
</td>
</tr>

<!--
<tr>
<td>
<input type="radio" name="today" value="" />Select a date manually :
<td>
Year<br>
<select name="year">
<option value="%" selected >All</option>
<option value="2014" >2014</option>
<option value="2015" >2015</option>
</select>
</td>
<td>
Month<br>
<select name="month">
<option value="%" selected>All</option>
<option value="01">Jan</option>
<option value="02">Feb</option>
<option value="03">Mar</option>
<option value="04">Apr</option>
<option value="05">May</option>
<option value="06">Jun</option>
<option value="07">Jul</option>
<option value="08">Aug</option>
<option value="09">Sep</option>
<option value="10">Oct</option>
<option value="11">Nov</option>
<option value="12">Dec</option>
</select>
</td>

<td>
Day<br>
<select name="day">
<option value="%" selected>All</option>
<option value="01">1</option>
<option value="02">2</option>
<option value="03">3</option>
<option value="04">4</option>
<option value="05">5</option>
<option value="06">6</option>
<option value="07">7</option>
<option value="08">8</option>
<option value="09">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
<option value="13">13</option>
<option value="14">14</option>
<option value="15">15</option>
<option value="16">16</option>
<option value="17">17</option>
<option value="18">18</option>
<option value="19">19</option>
<option value="20">20</option>
<option value="21">21</option>
<option value="22">22</option>
<option value="23">23</option>
<option value="24">24</option>
<option value="25">25</option>
<option value="26">26</option>
<option value="27">27</option>
<option value="28">28</option>
<option value="29">29</option>
<option value="30">30</option>
<option value="31">31</option>

</select>
</td>

</tr>
-->

</table>


<!--
Select Receiver: <br>
<input type="checkbox" class="rxid" name="selectallr"  id="selectallr" onClick="selectallCHBoxr();" value="TEST" checked disabled /><font color=#424242><label for="selectallr"></label>  Select All</font><br>
-->

<!--
<table>
<tr>
<td><input type="checkbox" id="rx1" name="rx1" class="rxid"  value="john-" onclick="manualr();" checked /><label for="rx1"></label> John </td>
<td><input type="checkbox" id="rx2" name="rx2" class="rxid"  value="Dorset" onclick="manualr();"  checked /><label for="rx2"></label>  Dorset</td>
<td><input type="checkbox" id="rx3" name="rx3" class="rxid" value="Dick" onclick="manualr();" checked /><label for="rx3"></label>  Dick </td>
<td><input type="checkbox" id="rx4" name="rx4" class="rxid"  value="Michael"  onclick="manualr();" checked /><label for="rx4"></label>  Michael</td>
<td><input type="checkbox" id="rx5" name="rx5" class="rxid"  value="KPC6NDB" onclick="manualr();" checked /><label for="rx5"></label>  KPC6NDB</td>
<td><input type="checkbox" id="rx18" name="rx18" class="rxid"  value="nl8811" onclick="manualr();" checked /><label for="rx18"></label> NL8811 </td>
</tr>
<tr>
<td><input type="checkbox" id="rx7" name="rx7" class="rxid"  value="dryden" onclick="manualr();" checked /><label for="rx7"></label>  Dryden </td>
<td><input type="checkbox" id="rx19" name="rx19" class="rxid"  value="majo88" onclick="manualr();" checked /><label for="rx19"></label> MAJO88BN </td>
<td><input type="checkbox" id="rx20" name="rx20" class="rxid"  value="py3crx" onclick="manualr();" checked /><label for="rx20"></label> PY3CRX </td>
<td><input type="checkbox" id="rx9" name="rx9" class="rxid"  value="dxa661" onclick="manualr();" checked /><label for="rx9"></label>  DXA661</td>
<td><input type="checkbox" id="rx17" name="rx17" class="rxid"  value="Chandler" onclick="manualr();" checked /><label for="rx17"></label> Chandler </td>
<td><input type="checkbox" id="rx12" name="rx12" class="rxid"  value="Kevin" onclick="manualr();" checked /><label for="rx12"></label>  Kevin</td>
</tr>
<tr>
<td><input type="checkbox" id="rx21" name="rx21" class="rxid"  value="john%arizona" onclick="manualr();" checked /><label for="rx21"></label> John/Arizona </td>
<td><input type="checkbox" id="rx13" name="rx13" class="rxid" value="ve1vdm" onclick="manualr();" checked /><label for="rx13"></label>  VE1VDM</td>
<td><input type="checkbox" id="rx14" name="rx14" class="rxid"  value="Steve" onclick="manualr();" checked /><label for="rx14"></label> Steve </td>
<td><input type="checkbox" id="rx15" name="rx15" class="rxid"  value="gm4slv" onclick="manualr();" checked /><label for="rx15"></label> GM4SLV </td>
<td><input type="checkbox" id="rx16" name="rx16" class="rxid"  value="Todd" onclick="manualr();" checked /><label for="rx16"></label> Todd </td>
<td><input type="checkbox" id="rx6" name="rx6" class="rxid"  value="perseus%bel" onclick="manualr();" checked /><label for="rx6"></label>  Dirk </td>
</tr>
<tr>
<td><input type="checkbox" id="rx8" name="rx8" class="rxid"  value="kbh" onclick="manualr();" checked /><label for="rx8"></label>  KBH </td>
<td><input type="checkbox" id="rx10" name="rx10" class="rxid"  value="Joachim" onclick="manualr();" checked /><label for="rx10"></label>  Joachim</td>
<td><input type="checkbox" id="rx11" name="rx11" class="rxid"  value="Martin" onclick="manualr();"  checked /><label for="rx11"></label> Martin</td>
</tr>
</table>
-->

<hr width=50%>
<tr>

Select freq: <br>
<input type="checkbox" class="freq" name="selectallf"  id="selectallf" onClick="selectallCHBoxf();" value="TEST" checked /><label for="selectallf"></label>  <font color=#424242>Select All</font><br>
<table>
<tr>
<td><input type="checkbox" id="f1" name="f1" class="freq" value="2177.0" onclick="manualf();" checked /><label for="f1"></label>  2177.0 </td>
<td><input type="checkbox" id="f2" name="f2" class="freq"  value="2182.0" onclick="manualf();" checked /><label for="f2"></label>  2182.0 </td>
</tr>
<tr>
<td><input type="checkbox" id="f3" name="f3" class="freq"  value="2187.5" onclick="manualf();" checked /><label for="f3"></label>  2187.5 </td>
<td><input type="checkbox" id="f4" name="f4" class="freq"  value="4207.5" onclick="manualf();" checked /><label for="f4"></label>  4207.5 </td>
<td><input type="checkbox" id="f5" name="f5" class="freq"  value="6312.0" onclick="manualf();"  checked /><label for="f5"></label>  6312.0 </td>
<td><input type="checkbox" id="f6" name="f6" class="freq"  value="8414.5" onclick="manualf();" checked /><label for="f6"></label>  8414.5 </td>
<td><input type="checkbox" id="f7" name="f7" class="freq"  value="12577.0"  onclick="manualf();" checked /><label for="f7"></label>  12577.0 </td>
<td><input type="checkbox" id="f8" name="f8" class="freq"  value="16804.5"  onclick="manualf();" checked /><label for="f8"></label>  16804.5 </td>
</tr>

</table>
<hr width=30%>
<table rules="cols" cellpadding="5">

<th>Format</th>
<th>Category</th>
<th>Telecommand<br>One</th>
<th>Telecommand<br>Two</th>
<th>Freq<br>/<br>Pos</th>

<th>EOS</th>
<th>ECC</th>





<tr>
<td>

<input type="radio" name="fmt" value="%" checked><font color=#424242>All</font><br>
<input type="radio" name="fmt"  value="area">102 Area Call<br>
<input type="radio" name="fmt"  value="dis">112 Distress<br>
<input type="radio" name="fmt"  value="grp">114 Common Interest<br>
<input type="radio" name="fmt"  value="all">116 All Ships<br>
<input type="radio" name="fmt"  value="sel">120 Individual Call<br>
<input type="radio" name="fmt"  value="auto">123 Semi-auto<br>

</td>

<td>

<input type="radio" name="cat" value="%" checked><font color=#424242>All</font><br>
<input type="radio" name="cat" value="rtn">100 Routine<br>
<input type="radio" name="cat" value="saf">108 Safety<br>
<input type="radio" name="cat" value="urg">110 Urgency<br>
<input type="radio" name="cat" value="dis">112 Distress<br>
<input type="radio" name="cat" value="unk">Unknown
</td>
<td>
<select name="tc1">
<option value="%" selected>All</option>
<option value="notest">Not TEST</option>
<option value="f3">100 F3E All TP</option>
<option value="f3%dup">101 F3E Duplex</option>
<option value="poll">103 Polling</option>
<option value="unable">104 Unable to comply</option>
<option value="end">105 End of Call</option>
<option value="data">106 Data</option>
<option value="j3e">109 J3E TP</option>
<option value="ack">110 Distress Ack</option>
<option value="relay">112 Distress Relay</option>
<option value="f1%fec">113 F1B FEC</option>
<option value="f1%arq">115 F1B ARQ</option>
<option value="test">118 Test</option>
<option value="pos">121 Pos. Update</option>
<option value="no%inf">126 No Info</option>
<option value="unk%err">Unknown/Error</option>
<option value="--">No TC1</option>
</select>
<td>
<select name="tc2">
<option value="%" selected>All</option>
<option value="reason">100 No Reason Given</option>
<option value="congestion">101 Congestion</option>
<option value="busy">102 Busy</option>
<option value="queue">103 Queue Indication</option>
<option value="barred">104 Station Barred</option>
<option value="no%oper">105 No Operator Available</option>
<option value="oper%unav">106 Operator Temp. Unavailable</option>
<option value="eq">107 Equipment Disabled</option>
<option value="unable%chan">108 Unable Channel</option>
<option value="unable%mode">109 Unable Mode</option>
<option value="conflict">110 Ships not parties to conflict</option>
<option value="medical">111 Medical Transports</option>
<option value="pay%phone">112 Payphone/Public call..</option>
<option value="fax%data">113 Facsimile/Data</option>
<option value="no%inf">126 No Info</option>
<option value="unk%err">Unknown/Error</option>
<option value="--">No TC2</option>
</select>
</td>
<td>
<input type="radio" name="fp" value="%" checked><font color=#424242>All</font><br>
<input type="radio" name="fp" value="fq">Freq<br>
<input type="radio" name="fp" value="pos">Pos

</td>
<td>

<input type="radio" name="eos" value="%" checked><font color=#424242>All</font><br>
<input type="radio" name="eos" value="req">117 RQ (Req)<br>
<input type="radio" name="eos" value="ack">122 BQ (Ack)<br>
<input type="radio" name="eos" value="eos">127 EOS<br>
<input type="radio" name="eos" value="unk%err">Unknown/Error

</td>


<td><font size="2">Only the last 24 hours<br>ERR are retained</font><br><br>
<input type="radio" name="cecc" value="ok" checked><font color=#424242>OK</font><br>
<input type="radio" name="cecc" value="err" >ERR<br>
<input type="radio" name="cecc" value="">OK & ERR
</select>
</td>

</tr>
</table>
<hr width=50%>
<table rules="cols">
<caption><input type="radio" name="both" value="sep" checked><font color=blue>Separate Stations</font></caption>

<th>To</th>
<!--<th><input type="radio" name="toormid" value="mid"><font color=#541b66>Use MID</font><br>
<br>To: MID</th>-->
<!--<th><input type="radio" name="toormid" value="from" checked><font color=#541b66>Use TO</font><br>
<br>To: Station</th>-->
<!--<th><br>And/Or</th>-->
<!--<th><input type="radio" name="fromormid" value="from" checked><font color=green>Use FROM</font><br>
<br>From: Station</th>-->
<th>From</th>
<!--<th><input type="radio" name="fromormid" value="mid"><font color=green>Use MID</font><br>
<br>From: MID</th> -->
<tr>

<!--
<td>
<select name="to_mid">
<option value="0" selected>All</option>
<option value="200">200/Eu</option>
<option value="300">300/NAm</option>
<option value="400">400/As-ME</option>
<option value="500">500/Au-SEAs</option>
<option value="600">600/Af</option>
<option value="700">700/SAm</option>
</select>
</td>
-->


<td>
<input type="radio" name="totype" value="COAST">Any Coast Station<br>
<input type="radio" name="totype" value="SHIP">Any Ship Station<br>
<input type="radio" name="totype" value="GROUP">Any Group MMSI<br><br>
<input type="radio" name="totype" value="" checked><input type="text" name="to_mmsi" /><br><font color=#424242 size="2pt">Enter a partial MMSI or Name<br>or leave blank for "all"</font><br><br>

<input type="radio" name="totype" value="MID">Specify Ship or Coast MID<br>
<hr>
<input type="radio" name = "tomidtype" value="COAST"checked>Coast
<input type="radio" name = "tomidtype" value="SHIP">Ship<br>
<input type="text" name="to_mid" /><br><font color=#424242 size="2pt">Enter a MID</font><br>

<!--<td><input type="radio" name="andor" value="and" checked><font color=#424242>AND</font>
<input type="radio" name="andor" value="or">OR<br>-->

</td>

<td>
<input type="radio" name="fromtype" value="COAST">Any Coast Station<br>
<input type="radio" name="fromtype" value="SHIP">Any Ship Station<br>
<input type="radio" name="fromtype" value="GROUP">Any Group MMSI<br><br>
<input type="radio" name="fromtype" value="" checked><input type="text" name="from_mmsi" /><br><font color=#424242 size="2pt">Enter a partial MMSI or name<br>or leave blank for "all"</font><br><br>
<input type="radio" name="fromtype" value="MID">Specify Ship or Coast MID<br>
<hr>
  <input type="radio" name = "frommidtype" value="COAST" checked>Coast
  <input type="radio" name = "frommidtype" value="SHIP">Ship<br>
<input type="text" name="from_mid" /><br><font color=#424242 size="2pt">Enter a MID</font><br>

<!--
<td>
<select name="from_mid">
<option value="0" selected>All</option>
<option value="200">200/Eu</option>
<option value="300">300/NAm</option>
<option value="400">400/As-ME</option>
<option value="500">500/Au-SEAs</option>
<option value="600">600/Af</option>
<option value="700">700/SAm</option>
</select>
</td>
-->

</tr>
</table>

<hr width=50%>
<table cellpadding=10 rules="cols">
<caption><input type="radio" name="both" value="both"><font color=blue>One Station</font></caption>

<th>Station as <i>either</i> Sender or Recipient</th>
<tr>

<td><input type="text" name="mmsi" /><br><font color=#424242 size="2pt">Enter a partial string<br>or leave blank for "all"</font></td>

</tr>
</table>
<hr width=50%>

<table rules="cols">

<th>Results<br>Range</th>
<th>Results<br>Order</th>
<tr>

<td>

<select name="limit">
<option value="0,1000000">All</option>
<option value="0, 100" selected>0-100</option>
<option value="100, 100">100-200</option>
<option value="200, 100">200-300</option>
<option value="300, 100">300-400</option>

</td>
<td>
<input type="radio" name="order" value="desc" checked><font color=#424242>Newest first</font><br>
<input type="radio" name="order" value="asc">Oldest first

</td></tr>

</table>
<hr width=50%>
<input id="link" type="submit" value="Search" />
<br>
<hr width=50%>
<input id="link" type="reset" value="Reset" />
</form>


</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>
