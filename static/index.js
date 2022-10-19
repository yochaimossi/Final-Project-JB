function getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }


$(document).ready(function()
{
    $('#departure_button').on('click', () => {

        let hours_num = parseInt($('#departure_delta').val())
        console.log(hours_num)

        $.ajax({url:"flights/departures/" + hours_num}).then(
            function(flights)
            {
                console.log(flights);
                // flights.sort((a, b) => a.departure_time - b.departure_time)
               
                let departures_table = $('#departures')
                departures_table.find("tr:gt(0)").remove()
            
                

                $.each(flights,  (i, flight) => {
        
                    departures_table.append(
                                `<tr><td class="fw-lighter">${flight.airline_company}</td>
                                     <td class="fw-lighter">${flight.origin_country}</td>
                                     <td class="fw-lighter">${flight.destination_country}</td>
                                     <td class="fw-lighter">${flight.departure_time}</td>
                                     <td class="fw-lighter">On time</td>`)
                                     
                })
            }
            ,function(err)
            {
                console.log(err);}
            );

    });


});


// show arrivals flights in table
$(document).ready(function()
{
    $('#arrival_button').on('click', () => {

        let hours_num = parseInt($('#arrival_delta').val())
        console.log(hours_num)

        $.ajax({url:"flights/arrivals/" + hours_num}).then(
            function(flights)
            {
                console.log(flights);
                // flights.sort((a, b) => a.departure_time - b.departure_time)
               
                let arrivals_table = $('#arrivals')
                arrivals_table.find("tr:gt(0)").remove()

                let rand_num
                let status
               
            
                $.each(flights,  (i, flight) => {
                    rand_num = getRandomInt(10)
                    if (rand_num === 1){
                        status = 'Delayed'
                    }
                    else{
                        status = 'On Time' 
                    }
        
                    arrivals_table.append(
                                `<tr><td class="fw-lighter">${flight.airline_company}</td>
                                     <td class="fw-lighter">${flight.origin_country}</td>
                                     <td class="fw-lighter">${flight.destination_country}</td>
                                     <td class="fw-lighter">${flight.landing_time}</td>
                                     <td class="fw-lighter">${status}</td>`)
                                     
                })
            }
            ,function(err)
            {
                console.log(err);}
            );

    });


});