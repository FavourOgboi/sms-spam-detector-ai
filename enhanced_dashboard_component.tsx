import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  Target, 
  Brain, 
  Users, 
  AlertTriangle,
  Info,
  CheckCircle,
  Clock
} from 'lucide-react';

interface ModelPerformanceProps {
  stats: {
    accuracyData: {
      trainingAccuracy: number;
      validationAccuracy: number;
      realTimeAccuracy: number | null;
    };
    totalMessages: number;
    avgConfidence: number;
    modelStats: any;
    recentPredictions: any[];
  };
}

const ModelPerformanceCard: React.FC<ModelPerformanceProps> = ({ stats }) => {
  const [selectedView, setSelectedView] = useState('overview');
  
  // Calculate performance insights
  const getPerformanceInsights = () => {
    const { trainingAccuracy, validationAccuracy, realTimeAccuracy } = stats.accuracyData;
    
    const insights = [];
    
    // Model stability check
    if (validationAccuracy && trainingAccuracy) {
      const overfitting = trainingAccuracy - validationAccuracy;
      if (overfitting > 0.05) {
        insights.push({
          type: 'warning',
          title: 'Potential Overfitting',
          message: `Training accuracy (${(trainingAccuracy * 100).toFixed(1)}%) is significantly higher than validation (${(validationAccuracy * 100).toFixed(1)}%)`,
          icon: AlertTriangle
        });
      } else {
        insights.push({
          type: 'success',
          title: 'Well-Generalized Model',
          message: 'Training and validation accuracies are well-balanced',
          icon: CheckCircle
        });
      }
    }
    
    // Real-world performance check
    if (realTimeAccuracy && validationAccuracy) {
      const realWorldDrift = validationAccuracy - realTimeAccuracy;
      if (realWorldDrift > 0.05) {
        insights.push({
          type: 'warning',
          title: 'Data Drift Detected',
          message: `Real-world performance (${(realTimeAccuracy * 100).toFixed(1)}%) is lower than expected. Consider retraining.`,
          icon: TrendingDown
        });
      } else if (realWorldDrift < -0.02) {
        insights.push({
          type: 'success',
          title: 'Excellent Real-World Performance',
          message: `Model performs better in practice than in testing!`,
          icon: TrendingUp
        });
      } else {
        insights.push({
          type: 'info',
          title: 'Stable Performance',
          message: 'Real-world performance matches expectations',
          icon: Target
        });
      }
    }
    
    // Confidence analysis
    if (stats.avgConfidence < 0.7) {
      insights.push({
        type: 'warning',
        title: 'Low Confidence Predictions',
        message: `Average confidence is ${(stats.avgConfidence * 100).toFixed(1)}%. Model may be uncertain.`,
        icon: AlertTriangle
      });
    }
    
    return insights;
  };
  
  const insights = getPerformanceInsights();
  
  // Get primary accuracy to display
  const getPrimaryAccuracy = () => {
    const { trainingAccuracy, validationAccuracy, realTimeAccuracy } = stats.accuracyData;
    
    if (realTimeAccuracy && stats.totalMessages >= 10) {
      return {
        value: realTimeAccuracy,
        label: 'Real-World Performance',
        type: 'realtime',
        samples: stats.totalMessages,
        description: 'Based on actual user feedback'
      };
    } else if (validationAccuracy) {
      return {
        value: validationAccuracy,
        label: 'Expected Performance',
        type: 'validation',
        description: 'Based on test dataset'
      };
    } else {
      return {
        value: trainingAccuracy,
        label: 'Training Performance',
        type: 'training',
        description: 'May be optimistic'
      };
    }
  };
  
  const primaryAccuracy = getPrimaryAccuracy();
  
  return (
    <div className="space-y-6">
      {/* Primary Performance Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            Model Performance Overview
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Primary Accuracy Display */}
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-4xl font-bold text-primary">
                  {(primaryAccuracy.value * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-muted-foreground">
                  {primaryAccuracy.label}
                </div>
                <Badge variant={primaryAccuracy.type === 'realtime' ? 'default' : 'secondary'}>
                  {primaryAccuracy.type === 'realtime' && <Users className="h-3 w-3 mr-1" />}
                  {primaryAccuracy.type === 'validation' && <Target className="h-3 w-3 mr-1" />}
                  {primaryAccuracy.type === 'training' && <Brain className="h-3 w-3 mr-1" />}
                  {primaryAccuracy.description}
                </Badge>
                {primaryAccuracy.samples && (
                  <div className="text-xs text-muted-foreground mt-1">
                    Based on {primaryAccuracy.samples} predictions
                  </div>
                )}
              </div>
              
              {/* Confidence Meter */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Average Confidence</span>
                  <span>{(stats.avgConfidence * 100).toFixed(1)}%</span>
                </div>
                <Progress value={stats.avgConfidence * 100} className="h-2" />
              </div>
            </div>
            
            {/* Quick Insights */}
            <div className="space-y-3">
              <h4 className="font-semibold text-sm">Performance Insights</h4>
              {insights.slice(0, 2).map((insight, index) => (
                <div key={index} className="flex items-start gap-2 p-3 rounded-lg bg-muted/50">
                  <insight.icon className={`h-4 w-4 mt-0.5 ${
                    insight.type === 'success' ? 'text-green-500' :
                    insight.type === 'warning' ? 'text-yellow-500' :
                    'text-blue-500'
                  }`} />
                  <div className="space-y-1">
                    <div className="text-sm font-medium">{insight.title}</div>
                    <div className="text-xs text-muted-foreground">{insight.message}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Detailed Analysis Tabs */}
      <Card>
        <CardHeader>
          <CardTitle>Detailed Performance Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={selectedView} onValueChange={setSelectedView}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="overview">Accuracy Breakdown</TabsTrigger>
              <TabsTrigger value="insights">AI Insights</TabsTrigger>
              <TabsTrigger value="trends">Performance Trends</TabsTrigger>
            </TabsList>
            
            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Training Accuracy */}
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Brain className="h-4 w-4 text-blue-500" />
                    <span className="font-medium">Training</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {(stats.accuracyData.trainingAccuracy * 100).toFixed(1)}%
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Performance on training data
                  </div>
                  <div className="text-xs text-yellow-600 mt-1">
                    ⚠️ May be optimistic
                  </div>
                </div>
                
                {/* Validation Accuracy */}
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Target className="h-4 w-4 text-green-500" />
                    <span className="font-medium">Validation</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {(stats.accuracyData.validationAccuracy * 100).toFixed(1)}%
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Expected real-world performance
                  </div>
                  <div className="text-xs text-green-600 mt-1">
                    ✓ Most reliable estimate
                  </div>
                </div>
                
                {/* Real-time Accuracy */}
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Users className="h-4 w-4 text-purple-500" />
                    <span className="font-medium">Real-World</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {stats.accuracyData.realTimeAccuracy 
                      ? `${(stats.accuracyData.realTimeAccuracy * 100).toFixed(1)}%`
                      : 'N/A'
                    }
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Actual user feedback
                  </div>
                  <div className="text-xs text-purple-600 mt-1">
                    {stats.accuracyData.realTimeAccuracy 
                      ? '🎯 Live performance'
                      : '⏳ Collecting feedback'
                    }
                  </div>
                </div>
              </div>
              
              {/* Explanation */}
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-start gap-2">
                  <Info className="h-4 w-4 text-blue-500 mt-0.5" />
                  <div className="text-sm">
                    <div className="font-medium text-blue-900 mb-1">Understanding Accuracy Types</div>
                    <div className="text-blue-700 space-y-1">
                      <div><strong>Training:</strong> How well the model learned from training data (may be optimistic)</div>
                      <div><strong>Validation:</strong> How well the model performs on unseen test data (most reliable)</div>
                      <div><strong>Real-World:</strong> How well the model performs on actual user data (can vary due to data differences)</div>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="insights" className="space-y-4">
              {insights.map((insight, index) => (
                <div key={index} className="flex items-start gap-3 p-4 border rounded-lg">
                  <insight.icon className={`h-5 w-5 mt-0.5 ${
                    insight.type === 'success' ? 'text-green-500' :
                    insight.type === 'warning' ? 'text-yellow-500' :
                    'text-blue-500'
                  }`} />
                  <div className="space-y-1">
                    <div className="font-medium">{insight.title}</div>
                    <div className="text-sm text-muted-foreground">{insight.message}</div>
                  </div>
                </div>
              ))}
            </TabsContent>
            
            <TabsContent value="trends" className="space-y-4">
              <div className="text-center py-8 text-muted-foreground">
                <Clock className="h-8 w-8 mx-auto mb-2" />
                <div>Performance trends will appear here as more data is collected</div>
                <div className="text-sm mt-1">Need at least 50 predictions to show trends</div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default ModelPerformanceCard;
