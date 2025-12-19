import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Schedule from './components/Schedule';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <Schedule />
      </main>
      <Footer />
    </div>
  );
}

export default App;
