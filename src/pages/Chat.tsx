import React, { useState } from "react";
import { MessageCircle, HelpCircle } from "lucide-react";

const spamFaqs = [
  {
    question: "What does a delivery scam message look like?",
    example: "USPS: Your package is pending delivery due to an unpaid shipping fee. Please update your information here to avoid return: [suspicious link]",
    tip: "Never click links or provide info unless you’re expecting a package and can verify the sender."
  },
  {
    question: "How do family emergency scam texts work?",
    example: "Hi Grandma, it’s your grandson. I got into a car accident and need money for the hospital, please send $500 to this CashApp: [CashApp ID]",
    tip: "Always verify with a phone call or another method before sending money."
  },
  {
    question: "What are signs of a fake prize or gift card message?",
    example: "Congratulations! You’ve won a $100 Amazon gift card! Click here to claim your prize now: [phishing link]",
    tip: "Legitimate giveaways rarely require a fee or sensitive info. Don’t click suspicious links."
  },
  {
    question: "How do overpayment/refund scams appear?",
    example: "You’ve overpaid $50 for a recent transaction. Click here to process your refund: [fake payment link]",
    tip: "Never provide bank details to unknown senders. Contact the company directly."
  },
  {
    question: "What are unknown group text scams?",
    example: "Hey everyone! Check out this amazing deal! [suspicious link]",
    tip: "Don’t click links or reply. Block and delete the group."
  },
  {
    question: "How do payment information scams work?",
    example: "Your [streaming service] account payment failed. Please update your payment details here to continue watching: [fake streaming service login link]",
    tip: "Go directly to the official website to check your account. Don’t use links in texts."
  },
  {
    question: "What are boss/colleague impersonation scams?",
    example: "Hi, it’s [Boss’s Name], and I need you to purchase $500 in gift cards as soon as possible for a client and send me the codes. Let me know when done.",
    tip: "Always verify unusual requests from your boss or colleagues through another channel."
  },
  {
    question: "What are suspicious activity alert scams?",
    example: "[Bank Name]: We’ve detected unusual login activity on your account. Verify it now: [phishing link]",
    tip: "Don’t click links. Contact your bank using the official number."
  },
  {
    question: "How do fake credit card offer scams work?",
    example: "You’ve been pre-approved for a platinum credit card with 0% APR for 18 months! Apply now: [fake application link]",
    tip: "Ignore unsolicited credit offers. Apply only through trusted sources."
  },
  {
    question: "What are job offer scam texts?",
    example: "URGENT HIRING! Earn $500/day working from home. No experience needed. Apply here: [scam job application link]",
    tip: "Be wary of offers that seem too good to be true or require upfront fees."
  },
  {
    question: "What are fake 2FA or verification code scams?",
    example: "Your [account name] verification code is: 123456. If you did not request this, secure your account here: [phishing link]",
    tip: "Don’t click links or share codes you didn’t request."
  },
  {
    question: "How do government agency scam texts work?",
    example: "IRS Notice: You have an outstanding tax issue. Immediate action is required to avoid penalties. Visit: [fake IRS website link]",
    tip: "Government agencies rarely contact you by text. Don’t click links or provide info."
  },
  {
    question: "What are subscription renewal scam texts?",
    example: "Your [streaming service] subscription will auto-renew for $99.99. Cancel now to avoid charges: [fake cancellation link]",
    tip: "Check your subscriptions directly. Don’t use links in texts."
  },
  {
    question: "How do fake debt collector scams work?",
    example: "URGENT: This is a final notice regarding an outstanding debt. Failure to pay will result in legal action. Contact us immediately at: [fake phone number] or visit: [suspicious link]",
    tip: "Verify debts with your creditor. Don’t pay or provide info to unknown contacts."
  },
  {
    question: "What are 'texts from your own number' scams?",
    example: "This is [cell phone service provider], and we’re sending a special offer to our loyal customers. Click here for more details! [suspicious link]",
    tip: "Ignore texts from your own number. It’s a spoofing scam."
  },
  {
    question: "How do bank account verification scams work?",
    example: "This is [Bank Name]. For security reasons, please verify your account information: [phishing link]",
    tip: "Contact your bank directly. Don’t use links in texts."
  },
  {
    question: "What are cryptocurrency scam texts?",
    example: "Insiders say [Cryptocurrency] is about to explode in value. Buy now while the price is still low: [scam cryptocurrency link]",
    tip: "Ignore investment offers from unknown sources. Don’t click links."
  },
  {
    question: "How do utility bill scam texts work?",
    example: "Your electricity service will be disconnected due to non-payment. Pay now: [fake payment link]",
    tip: "Contact your utility provider directly. Don’t pay through links in texts."
  },
  {
    question: "What are overdue toll fee scam texts?",
    example: "E-Toll Alert: You have an outstanding balance. Pay immediately to avoid penalties: [fake toll payment website]",
    tip: "Check your toll account directly. Don’t use links in texts."
  },
  {
    question: "How do account reactivation scam texts work?",
    example: "Your [social media platform] account has been temporarily locked. Reactivate it here: [fake login link]",
    tip: "Go to the official website to check your account. Don’t use links in texts."
  }
];

const Chat: React.FC = () => {
  const [selectedFaq, setSelectedFaq] = useState<number | null>(null);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8 px-2 sm:px-4">
      {/* Section 1: Upcoming AI Chatbot */}
      <div className="bg-white rounded-2xl shadow-xl p-10 flex flex-col items-center mb-10">
        <div className="p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mb-4">
          <MessageCircle className="w-12 h-12 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-gray-800 mb-2">AI Chatbot (Upcoming)</h1>
        <p className="text-gray-600 text-center mb-4">
          This section is reserved for a future AI-powered assistant.<br />
          The intention is to provide users with a smart, interactive chatbot that can answer questions, offer guidance, and help you stay safe from SMS spam and scams.<br />
          Please check back in a future update!
        </p>
        <span className="inline-block px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
          Coming Soon 🚀
        </span>
      </div>

      {/* Section 2: FAQ/DAQ */}
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl">
        <div className="flex items-center mb-4">
          <HelpCircle className="w-6 h-6 text-blue-500 mr-2" />
          <h2 className="text-xl font-bold text-gray-800">Frequently Asked Questions (SMS Spam Types)</h2>
        </div>
        <div className="space-y-2">
          {spamFaqs.map((faq, idx) => (
            <div key={idx} className="mb-2">
              <button
                className={`w-full text-left px-4 py-2 rounded-lg border ${selectedFaq === idx ? "bg-blue-50 border-blue-300" : "bg-gray-50 border-gray-200"} hover:bg-blue-100 transition-colors font-medium`}
                onClick={() => setSelectedFaq(selectedFaq === idx ? null : idx)}
              >
                {faq.question}
              </button>
              {selectedFaq === idx && (
                <div className="mt-2 ml-2 p-4 bg-blue-50 rounded-lg border border-blue-100">
                  <div className="mb-2">
                    <span className="font-semibold text-gray-700">Example:</span>
                    <span className="ml-2 text-gray-700">{faq.example}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-700">Tip:</span>
                    <span className="ml-2 text-blue-800">{faq.tip}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Chat;
