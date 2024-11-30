function onClose(){
    document.getElementById("alert").style.display = "none";
}

function fetchData(){
    const date_filter = document.getElementById('date_filter');
    const week_input = document.getElementById('week_number');
    const [year, month] = date_filter.value.split('-');
    const week = week_input.value;
    fetch(`/work-shifts?month=${month}&year=${year}&week=${week}`)
      .then((res) => {
        if(!res.ok){
          throw new Error('Network response was not ok');
        }
        return res.text();
      })
      .then(html =>{
        document.getElementById('content').innerHTML = html;
      })
      .catch((err) => console.log(err))
}