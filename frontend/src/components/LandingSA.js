import React from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import SAFlag from './assets/sa-flag.png';

const LandingSA = () => {
  const testimonials = [
    {
      name: "Thabo M.",
      business: "Spaza Shop, Soweto",
      quote: "This AI helped me automate orders via WhatsApp - sales up 40%!"
    },
    {
      name: "Lerato K.",
      business: "Beauty Salon, Cape Town",
      quote: "Finally, affordable tech made for SA small businesses"
    }
  ];

  const pricing = [
    {
      plan: "Starter",
      price: "R199/mo",
      features: ["Basic WhatsApp bot", "5 social posts/mo", "Email support"]
    },
    {
      plan: "Business",
      price: "R499/mo",
      features: ["Advanced AI tools", "Unlimited posts", "Priority support", "SA VAT included"]
    }
  ];

  return (
    <div className="landing-sa">
      {/* Hero Section with Local Flair */}
      <section className="sa-hero">
        <Row>
          <Col md={6}>
            <h1>
              <img src={SAFlag} alt="SA Flag" className="flag-icon" /> 
              AI Solutions Built for South Africa
            </h1>
            <p className="lead">
              Automate your business the smart way - designed for SA's unique challenges
            </p>
            <div className="cta-buttons">
              <Button variant="primary" size="lg">
                Free Demo (No CC Required)
              </Button>
              <Button variant="outline-secondary" size="lg">
                WhatsApp Chat
              </Button>
            </div>
            <div className="trust-badges">
              <p>Featured in: <span>Business Day</span> • <span>702</span> • <span>Entrepreneur SA</span></p>
            </div>
          </Col>
          <Col md={6}>
            {/* Video placeholder with local imagery */}
          </Col>
        </Row>
      </section>

      {/* Local Proof Section */}
      <section className="local-proof">
        <h2>Trusted by South African Businesses</h2>
        <Row>
          {testimonials.map((testimonial, index) => (
            <Col md={6} key={index}>
              <div className="testimonial-card">
                <p>"{testimonial.quote}"</p>
                <div className="author">
                  <strong>{testimonial.name}</strong>
                  <span>{testimonial.business}</span>
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </section>

      {/* Pricing in ZAR */}
      <section className="pricing">
        <h2>Simple Pricing for SA Budgets</h2>
        <Row>
          {pricing.map((plan, index) => (
            <Col md={6} key={index}>
              <div className="pricing-card">
                <h3>{plan.plan}</h3>
                <div className="price">{plan.price}</div>
                <ul>
                  {plan.features.map((feature, i) => (
                    <li key={i}>{feature}</li>
                  ))}
                </ul>
                <Button variant={index === 1 ? "primary" : "outline-primary"}>
                  Choose Plan
                </Button>
              </div>
            </Col>
          ))}
        </Row>
        <div className="pricing-note">
          <p>Special launch discount - 20% off first 3 months for the first 100 signups!</p>
        </div>
      </section>

      {/* Local Payment Options */}
      <section className="payment-options">
        <h4>We Accept:</h4>
        <div className="payment-methods">
          <span>Credit Cards</span>
          <span>EFT</span>
          <span>SnapScan</span>
          <span>M-Pesa</span>
        </div>
      </section>
    </div>
  );
};

export default LandingSA;
