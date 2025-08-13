import React, { useState, useEffect } from 'react';
import { Row, Col, Card, ProgressBar, Table } from 'react-bootstrap';
import { ZAR } from 'react-currency-format';

const SAMarketingDashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    signups: 0,
    target: 100,
    daysRemaining: 7,
    bestPerformingChannel: '',
    conversionRate: 0,
    zarSpent: 0
  });

  const [campaigns, setCampaigns] = useState([
    { id: 1, name: 'Facebook SA Groups', cost: 1500, conversions: 12, roi: 3.2 },
    { id: 2, name: 'WhatsApp Blast', cost: 800, conversions: 28, roi: 6.5 },
    { id: 3, name: 'Local Influencers', cost: 2500, conversions: 19, roi: 2.1 }
  ]);

  useEffect(() => {
    // Simulate data fetching
    const interval = setInterval(() => {
      setDashboardData(prev => ({
        ...prev,
        signups: Math.min(prev.signups + Math.floor(Math.random() * 5), prev.target),
        daysRemaining: 7 - Math.floor((new Date() - new Date('2023-11-01')) / (1000 * 60 * 60 * 24)),
        bestPerformingChannel: ['Facebook', 'WhatsApp', 'Referrals'][Math.floor(Math.random() * 3)],
        conversionRate: prev.conversionRate + (Math.random() * 0.5 - 0.2),
        zarSpent: prev.zarSpent + Math.random() * 500
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const calculateDailyTarget = () => {
    const targetPerDay = dashboardData.target / 7;
    const achievedToday = dashboardData.signups / (7 - dashboardData.daysRemaining);
    return {
      target: targetPerDay,
      current: achievedToday
    };
  };

  return (
    <div className="sa-marketing-dashboard">
      <h2>South Africa Launch Campaign</h2>
      <p className="text-muted">
        Goal: {dashboardData.signups}/{dashboardData.target} signups • 
        {dashboardData.daysRemaining} days remaining
      </p>

      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Signup Progress</Card.Title>
              <ProgressBar 
                now={(dashboardData.signups / dashboardData.target) * 100} 
                label={`${dashboardData.signups}/${dashboardData.target}`}
                variant={dashboardData.signups >= dashboardData.target * 0.7 ? 'success' : 
                        dashboardData.signups >= dashboardData.target * 0.4 ? 'warning' : 'danger'}
              />
              <div className="mt-3">
                <strong>Daily Target:</strong> {Math.round(calculateDailyTarget().current)}/
                {Math.round(calculateDailyTarget().target)}
                <ProgressBar 
                  now={(calculateDailyTarget().current / calculateDailyTarget().target) * 100}
                  className="mt-1"
                  style={{ height: '8px' }}
                />
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Quick Stats</Card.Title>
              <Row>
                <Col>
                  <div className="stat-box">
                    <h3>{dashboardData.conversionRate.toFixed(1)}%</h3>
                    <small>Conversion Rate</small>
                  </div>
                </Col>
                <Col>
                  <div className="stat-box">
                    <h3><ZAR value={dashboardData.zarSpent} displayType={'text'} /></h3>
                    <small>Total Spend</small>
                  </div>
                </Col>
                <Col>
                  <div className="stat-box">
                    <h3>{dashboardData.bestPerformingChannel}</h3>
                    <small>Top Channel</small>
                  </div>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Campaign Performance</Card.Title>
          <Table striped hover>
            <thead>
              <tr>
                <th>Campaign</th>
                <th>Cost (ZAR)</th>
                <th>Signups</th>
                <th>ROI</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {campaigns.map(campaign => (
                <tr key={campaign.id}>
                  <td>{campaign.name}</td>
                  <td><ZAR value={campaign.cost} displayType={'text'} /></td>
                  <td>{campaign.conversions}</td>
                  <td>{campaign.roi.toFixed(1)}x</td>
                  <td>
                    <span className={`badge ${
                      campaign.roi > 4 ? 'bg-success' : 
                      campaign.roi > 2 ? 'bg-warning' : 'bg-danger'
                    }`}>
                      {campaign.roi > 4 ? 'Excellent' : 
                       campaign.roi > 2 ? 'Moderate' : 'Needs Work'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Card>
        <Card.Body>
          <Card.Title>Recommended Actions</Card.Title>
          <ul className="action-list">
            {dashboardData.signups < dashboardData.target * 0.3 && (
              <li>🚀 <strong>Boost top-performing channels:</strong> Increase budget for WhatsApp campaigns by 30%</li>
            )}
            {dashboardData.daysRemaining < 3 && dashboardData.signups < dashboardData.target * 0.7 && (
              <li>🔥 <strong>Activate emergency referral bonus:</strong> Offer R300 cash for referrals this week</li>
            )}
            <li>📱 <strong>Schedule afternoon WhatsApp blast:</strong> Target inactive leads from signup form</li>
            <li>📻 <strong>Contact local radio stations:</strong> Pitch interview about AI for township businesses</li>
          </ul>
        </Card.Body>
      </Card>
    </div>
  );
};

export default SAMarketingDashboard;
