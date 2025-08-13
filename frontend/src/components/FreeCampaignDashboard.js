import React, { useState, useEffect } from 'react';
import { ProgressBar, Card, Table, Badge } from 'react-bootstrap';

const FreeCampaignDashboard = () => {
  const [data, setData] = useState({
    signups: 57,
    target: 100,
    sources: [
      { name: 'Facebook Groups', signups: 23, effort: 'High' },
      { name: 'Twitter', signups: 12, effort: 'Medium' },
      { name: 'Referrals', signups: 9, effort: 'Low' },
      { name: 'Forums', signups: 7, effort: 'High' },
      { name: 'Influencers', signups: 6, effort: 'Medium' }
    ],
    conversionRate: 34.2
  });

  const calculateROE = (signups, effort) => {
    const effortScore = { 'High': 3, 'Medium': 2, 'Low': 1 }[effort];
    return (signups / effortScore).toFixed(1);
  };

  return (
    <div className="free-campaign-dashboard">
      <h3>Zero-Cost Acquisition Campaign</h3>
      
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Progress Overview</Card.Title>
          <div className="mb-3">
            <strong>{data.signups}/{data.target}</strong> signups achieved
            <ProgressBar 
              now={(data.signups / data.target) * 100} 
              variant={data.signups > 70 ? "success" : data.signups > 40 ? "warning" : "danger"}
              className="mt-2"
            />
          </div>
          <div>
            <strong>Conversion Rate:</strong> {data.conversionRate}%
            <ProgressBar 
              now={data.conversionRate} 
              max={100}
              variant={data.conversionRate > 30 ? "success" : data.conversionRate > 15 ? "warning" : "danger"}
              className="mt-2"
            />
          </div>
        </Card.Body>
      </Card>
      
      <Card>
        <Card.Body>
          <Card.Title>Channel Performance</Card.Title>
          <Table striped hover>
            <thead>
              <tr>
                <th>Channel</th>
                <th>Signups</th>
                <th>Effort</th>
                <th>ROE*</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {data.sources.map((source, index) => (
                <tr key={index}>
                  <td>{source.name}</td>
                  <td>{source.signups}</td>
                  <td>
                    <Badge bg={
                      source.effort === 'High' ? 'danger' : 
                      source.effort === 'Medium' ? 'warning' : 'success'
                    }>
                      {source.effort}
                    </Badge>
                  </td>
                  <td>{calculateROE(source.signups, source.effort)}</td>
                  <td>
                    {parseFloat(calculateROE(source.signups, source.effort)) > 5 ? (
                      <span className="text-success">Double Down</span>
                    ) : (
                      <span className="text-warning">Optimize</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <small className="text-muted">*ROE = Return on Effort (Signups per Effort Unit)</small>
          
          <div className="recommendations mt-3">
            <h5>Recommended Actions:</h5>
            <ul>
              <li>Focus more on <strong>Referrals</strong> (High ROE)</li>
              <li>Improve or reduce <strong>Forums</strong> (Low ROE)</li>
              <li>Create shareable content for <strong>Facebook Groups</strong></li>
            </ul>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default FreeCampaignDashboard;
