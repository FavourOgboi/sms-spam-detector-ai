import React from 'react';
import { Outlet } from 'react-router-dom';
import Navigation from './Navigation';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navigation />
      {/* Main Content */}
      <div className="md:ml-64 flex-1 flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Page Content */}
        <main className="flex-1 p-6 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
