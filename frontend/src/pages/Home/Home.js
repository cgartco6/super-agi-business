import React from 'react';
import { Header, ServiceCard, Testimonials, CTA } from '../../components';
import './Home.css';

const Home = () => {
  const services = [
    {
      title: "Chatbot Creation",
      tiers: [
        { level: "Basic", price: "$99", features: ["Simple Q&A", "Basic integration"] },
        { level: "Advanced", price: "$499", features: ["AI-powered", "Multi-platform"] }
      ]
    },
    // Additional services...
  ];

  return (
    <div className="home-page">
      <Header />
      
      <section className="hero">
        <h1>AI-Powered Digital Solutions</h1>
        <p>Automated, secure, and professional services tailored to your needs</p>
        <CTA text="Get Started" link="/services" />
      </section>
      
      <section className="services-preview">
        <h2>Our Services</h2>
        <div className="service-grid">
          {services.map((service, index) => (
            <ServiceCard key={index} service={service} />
          ))}
        </div>
      </section>
      
      <Testimonials />
      
      <section className="contact-cta">
        <h2>Ready to Transform Your Business?</h2>
        <CTA text="Contact Us" link="/contact" variant="secondary" />
      </section>
    </div>
  );
};

export default Home;
