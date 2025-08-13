import React from 'react';
import { Button, Row, Col, Alert } from 'react-bootstrap';
import SAFlag from './assets/sa-flag.png';

const FreeOfferSA = () => {
  const [countdown, setCountdown] = useState({
    days: 7,
    hours: 23,
    minutes: 59,
    spotsLeft: 43
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        const newMins = prev.minutes - 1;
        const newHours = newMins < 0 ? prev.hours - 1 : prev.hours;
        const newDays = newHours < 0 ? prev.days - 1 : prev.days;
        
        return {
          days: newDays,
          hours: newHours < 0 ? 23 : newHours,
          minutes: newMins < 0 ? 59 : newMins,
          spotsLeft: prev.spotsLeft - Math.floor(Math.random() * 3)
        };
      });
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  const socialProof = [
    { name: "Thando N.", location: "Soweto", quote: "Got 28 new clients using the free WhatsApp tools!" },
    { name: "Jaco V.", location: "Pretoria", quote: "Automated my consultations with zero coding" },
    { name: "Lerato K.", location: "Durban", quote: "Finally tech made for SA small business needs" }
  ];

  return (
    <div className="free-offer-sa">
      <Row className="align-items-center">
        <Col md={6}>
          <h1>
            <img src={SAFlag} alt="SA Flag" className="flag-icon" /> 
            <strong>Free</strong> AI Tools for SA Businesses
          </h1>
          
          <Alert variant="warning" className="mt-3">
            <strong>Limited Offer:</strong> First 100 signups get 3 months free access
          </Alert>
          
          <div className="countdown-box mb-4">
            <h5>Offer Ends In:</h5>
            <div className="countdown-timer">
              <span>{countdown.days}d</span> : 
              <span>{countdown.hours}h</span> : 
              <span>{countdown.minutes}m</span>
            </div>
            <small className="text-muted">{countdown.spotsLeft} spots remaining</small>
          </div>
          
          <ul className="benefits-list">
            <li>✓ WhatsApp automation for customer queries</li>
            <li>✓ Social media scheduling tool</li>
            <li>✓ Basic AI chatbot for your website</li>
            <li>✓ Made for SA business needs</li>
            <li>✓ No credit card required</li>
          </ul>
          
          <Button variant="success" size="lg" className="mt-3">
            Claim Free Access Now
          </Button>
          
          <div className="trust-signals mt-3">
            <small className="text-muted">
              Already joined by 57 South African businesses
            </small>
          </div>
        </Col>
        
        <Col md={6}>
          <div className="testimonial-carousel">
            {socialProof.map((testimonial, index) => (
              <div key={index} className="testimonial-card">
                <p>"{testimonial.quote}"</p>
                <div className="author">
                  <strong>{testimonial.name}</strong>
                  <span>{testimonial.location}</span>
                </div>
              </div>
            ))}
          </div>
          
          <div className="social-proof-logos mt-4">
            <p>Featured on:</p>
            <div className="logos">
              <span>SA Business Daily</span>
              <span>Entrepreneur SA</span>
              <span>TechCentral</span>
            </div>
          </div>
        </Col>
      </Row>
      
      <Row className="mt-5">
        <Col>
          <div className="viral-referral-box">
            <h4>Want <strong>extra free months?</strong></h4>
            <p>
              Share this offer and get +1 free month for every 3 friends who sign up!
            </p>
            <Button variant="outline-primary">
              Get Shareable Link
            </Button>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default FreeOfferSA;
