import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
        
        // lab9
        fetch(`http://acit3855lab6.eastus.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>New Cases</th>
							<th>Newly Vaccinated</th>
						</tr>
						<tr>
							<td># New Cases: {stats['num_new_cases_readings']}</td>
							<td># Newly Vaccinated: {stats['num_newly_vaccinated_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Longest Patient Name: {stats['longest_patient_name']}</td>
						</tr>
						<tr>
							<td colspan="2">Shortest Patient Name: {stats['shortest_patient_name']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_Updated']}</h3>

            </div>
        )
    }
}