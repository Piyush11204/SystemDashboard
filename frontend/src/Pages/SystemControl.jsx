import  { useState, useEffect, useCallback } from 'react';
import { Server,  Network, Power, Activity } from 'lucide-react';
import axios from 'axios';

const SystemControlDashboard = () => {
  const [systemInfo, setSystemInfo] = useState([]);
  const [processList, setProcessList] = useState([]);
  const [networkInfo, setNetworkInfo] = useState(null);
  const [loading, setLoading] = useState({
    systemInfo: false,
    processList: false,
    networkInfo: false,
    appControl: false,
    controlActions: false,
  });
  const [error, setError] = useState(null);

  // Handle errors
  const handleError = useCallback((errorMessage, context) => {
    console.error(`${context} Error:`, errorMessage);
    setError({
      message: errorMessage,
      context: context,
    });
  }, []);
  
  
  // Fetch data from the backend API
  const fetchData = useCallback(async (endpoint, setDataCallback, loadingKey) => {
    setLoading((prev) => ({ ...prev, [loadingKey]: true }));
    setError(null);

    try {
      const response = await axios.get(`http://localhost:5000/api/system-control/${endpoint}`);
      setDataCallback(response.data);
    } catch (err) {
      handleError(err.message, endpoint);
    } finally {
      setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    }
  }, [handleError]);

  // Handle control actions
  const handleControlAction = async (action) => {
    setLoading((prev) => ({ ...prev, controlActions: true }));
    
    try {
      const response = await axios.post('http://localhost:5000/api/system-control', { command: action });
      alert(response.data.message); // Display success message
    } catch (err) {
      handleError(err.message, 'Control Action');
    } finally {
      setLoading((prev) => ({ ...prev, controlActions: false }));
    }
  };

  // Use effect hook to fetch initial data
  useEffect(() => {
    fetchData('info', setSystemInfo, 'systemInfo');

    fetchData('processes', setProcessList, 'processList');
    fetchData('network', setNetworkInfo, 'networkInfo');
  }, [fetchData]);

  // Render system info card
  const renderSystemInfoCard = () => (
    <div className="bg-white shadow-md rounded-lg p-4">
      <div className="flex items-center mb-4">
        <Server className="mr-2 text-blue-500" />
        <h2 className="text-xl font-semibold">System Information</h2>
      </div>
      {systemInfo ? (
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div><strong>OS:</strong> {systemInfo.os}</div>
          <div><strong>Processor:</strong> {systemInfo.processor}</div>
          <div><strong>Memory:</strong> {systemInfo.memory_total}</div>
          <div><strong>CPU Cores:</strong> {systemInfo.cpu_cores}</div>
        </div>
      ) : (
        <p>Loading system information...</p>
      )}
    </div>
  );

  // Render process list card
  const renderProcessListCard = () => (
    <div className="bg-white shadow-md rounded-lg p-4">
      <div className="flex items-center mb-4">
        <Activity className="mr-2 text-green-500" />
        <h2 className="text-xl font-semibold">Running Processes</h2>
      </div>
      {processList.length > 0 ? (
        <div className="max-h-64 overflow-y-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">Name</th>
                <th className="py-2 px-4 border-b">PID</th>
                <th className="py-2 px-4 border-b">Status</th>
              </tr>
            </thead>
            <tbody>
              {processList.map((process) => (
                <tr key={process.pid}>
                  <td className="py-2 px-4 border-b">{process.name}</td>
                  <td className="py-2 px-4 border-b">{process.pid}</td>
                  <td className="py-2 px-4 border-b">{process.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Loading process list...</p>
      )}
    </div>
  );

  // Render network info card
  const renderNetworkInfoCard = () => (
    <div className="bg-white shadow-md rounded-lg p-4">
      <div className="flex items-center mb-4">
        <Network className="mr-2 text-yellow-500" />
        <h2 className="text-xl font-semibold">Network Information</h2>
      </div>
      {networkInfo ? (
        <div className="text-sm">
          <div><strong>IP Address:</strong> {networkInfo.ip}</div>
          <div><strong>Interfaces:</strong> {networkInfo.interfaces.join(', ')}</div>
          <div><strong>Internet Connectivity:</strong> {networkInfo.internet_connectivity ? 'Connected' : 'Not Connected'}</div>
        </div>
      ) : (
        <p>Loading network information...</p>
      )}
    </div>
  );

  // Render control actions section
  const renderControlActions = () => {
    const controlActions = [
      'open browser',
      'close browser',
      'open edge',
      'open firefox',
      'open notepad',
      'open terminal',
      'open vscode',
      'system info',
      'get processes',
      'network status',
      'restart computer',
      'shutdown',
      'sleep',
      'clear memory cache',
      'end high cpu process',
      'take screenshot',
      'show desktop',
      'lock computer',
    ];

    return (
      <div className="bg-white shadow-md rounded-lg p-4">
        <div className="flex items-center mb-4">
          <Power className="mr-2 text-red-500" />
          <h2 className="text-xl font-semibold">Control Actions</h2>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {controlActions.map((action) => (
            <button
              key={action}
              onClick={() => handleControlAction(action)}
              className="bg-blue-500 text-white py-2 px-4 rounded"
              disabled={loading.controlActions}
            >
              {loading.controlActions ? 'Processing...' : action}
            </button>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4 p-6">
      <h1 className="text-2xl font-bold text-center">System Control Dashboard</h1>
      
      {error && (
        <div className="bg-red-500 text-white p-4 rounded">
          <strong>Error:</strong> {error.context} - {error.message}
        </div>
      )}
      
      {renderControlActions()}
      {renderSystemInfoCard()}
      {renderNetworkInfoCard()}
      {renderProcessListCard()}
    </div>
  );
};

export default SystemControlDashboard;