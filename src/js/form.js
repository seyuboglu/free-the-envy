

function clicked() {
    var agent_to_valuations = {};
    var p1name = document.getElementById('p1name').value;
    var p1vals = [];
    var p1room1 = document.getElementById('p1room1').value;
    p1vals.push(p1room1);
    var p1room2 = document.getElementById('p1room2').value;
    p1vals.push(p1room2);
    var p1room3 = document.getElementById('p1room3').value;
    p1vals.push(p1room3);
    agent_to_valuations[p1name] = p1vals

    var p2name = document.getElementById('p2name').value;
    var p2vals = [];
    var p2room1 = document.getElementById('p2room1').value;
    p2vals.push(p2room1);
    var p2room2 = document.getElementById('p2room2').value;
    p2vals.push(p2room2);
    var p2room3 = document.getElementById('p2room3').value;
    p2vals.push(p2room3);
    agent_to_valuations[p2name] = p2vals

    var p3name = document.getElementById('p3name').value;
    var p3vals = [];
    var p3room1 = document.getElementById('p3room1').value;
    p3vals.push(p3room1);
    var p3room2 = document.getElementById('p3room2').value;
    p3vals.push(p3room2);
    var p3room3 = document.getElementById('p3room3').value;
    p3vals.push(p3room3);
    agent_to_valuations[p3name] = p3vals

    var response =  { "n": 3, "total_rent": 1000, "method": "PriceFairnessMethod", "agent_to_valuations" : agent_to_valuations}

    // let form = document.createElement('form');
    // form.action = 'https://google.com/search';
    // form.method = 'GET';
    //
    // form.innerHTML = '<input name="q" value="test">';

    // the form must be in the document to submit it


    doWork(response)
}

function doWork(response) {
  // ajax the JSON to the server
  $.post("receiver", response, function(){

  });
  // stop link reloading the page
 event.preventDefault();
}

document.getElementById('btn').addEventListener('click', clicked);
