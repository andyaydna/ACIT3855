import logo from './logo.png';
import './App.css';

import EndpointAudit from './components/EndpointAudit'
import AppStats from './components/AppStats'

function App() {

    // lab 9
    const endpoints = ["tracker/get_new_cases", "tracker/get_new_vaccinated"]

    const rendered_endpoints = endpoints.map((endpoint) => {
        return <EndpointAudit key={endpoint} endpoint={endpoint}/>
    })

    return (
        <div className="App">
            <img src={logo} className="App-logo" alt="logo" height="150px" width="400px"/>
            <div>
                <AppStats/>
                <h1>Audit Endpoints</h1>
                {rendered_endpoints}
            </div>
        </div>
    );

}

export default App;