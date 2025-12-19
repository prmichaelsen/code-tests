# TrafficChart Component Design

## Overview
A Chart.js bar chart component that visualizes average store traffic data by day of the week. Displays in the LocationModal when `avgStoreTraffic` data is available.

## Visual Design
- **Type**: Bar chart
- **Size**: Full width of modal body, ~250px height
- **Colors**: Blue bars (#4285F4)
- **Labels**: Days of week (Mon-Sun)
- **Grid**: Light gray gridlines

## Props Interface
```typescript
interface TrafficChartProps {
  data: {
    monday: number | null;
    tuesday: number;
    wednesday: number;
    thursday: number;
    friday: number;
    saturday: number;
    sunday: number;
  };
  className?: string;
}
```

## Data Transformation
```typescript
const transformTrafficData = (data: TrafficData) => {
  return {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Visitors',
        data: [
          data.monday ?? 0,
          data.tuesday,
          data.wednesday,
          data.thursday,
          data.friday,
          data.saturday,
          data.sunday,
        ],
        backgroundColor: '#4285F4',
        borderColor: '#3367D6',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };
};
```

## Chart Configuration
```typescript
const chartOptions: ChartOptions<'bar'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: false,
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: {
        size: 14,
      },
      bodyFont: {
        size: 13,
      },
      callbacks: {
        label: (context) => {
          return `Visitors: ${context.parsed.y}`;
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0,
      },
      grid: {
        color: '#e5e7eb',
      },
    },
    x: {
      grid: {
        display: false,
      },
    },
  },
};
```

## Component Implementation
```typescript
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const TrafficChart: React.FC<TrafficChartProps> = ({ data, className }) => {
  const chartData = transformTrafficData(data);

  return (
    <div className={`traffic-chart ${className || ''}`}>
      <Bar data={chartData} options={chartOptions} height={250} />
    </div>
  );
};
```

## Styling
```css
.traffic-chart {
  width: 100%;
  height: 250px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 6px;
}

.chart-wrapper {
  position: relative;
  height: 100%;
}
```

## Data Handling
- Handle `null` values (e.g., monday: null) by displaying as 0
- Show "N/A" or skip day if no data available
- Format large numbers with commas (1,918 instead of 1918)
- Calculate and show average traffic (optional)

## Enhanced Features (Optional)
```typescript
// Calculate statistics
const calculateStats = (data: TrafficData) => {
  const values = Object.values(data).filter((v): v is number => v !== null);
  const total = values.reduce((sum, val) => sum + val, 0);
  const average = Math.round(total / values.length);
  const max = Math.max(...values);
  const min = Math.min(...values);

  return { total, average, max, min };
};

// Display stats above chart
<div className="traffic-stats">
  <div className="stat">
    <span className="stat-label">Average:</span>
    <span className="stat-value">{stats.average}</span>
  </div>
  <div className="stat">
    <span className="stat-label">Peak:</span>
    <span className="stat-value">{stats.max}</span>
  </div>
</div>
```

## Accessibility
- `aria-label="Average store traffic by day"`
- Chart.js provides keyboard navigation
- Tooltips show exact values on hover
- Color contrast meets WCAG standards

## Performance
- Memoize chart data transformation
- Use `React.memo` to prevent unnecessary re-renders
- Lazy load Chart.js if not needed initially

## Error Handling
```typescript
if (!data || Object.keys(data).length === 0) {
  return (
    <div className="no-chart-data">
      <p>No traffic data available</p>
    </div>
  );
}
```

## Example Data
```typescript
// From sample-data.js
avgStoreTraffic: {
  monday: null,
  tuesday: 504,
  wednesday: 607,
  thursday: 705,
  friday: 714,
  saturday: 1918,  // Peak day
  sunday: 1295
}
```

## Chart Variations (Optional)
- **Line Chart**: Show trends over time
- **Doughnut Chart**: Show distribution percentages
- **Mixed Chart**: Compare multiple locations

## Dependencies
- `chart.js` - Chart library
- `react-chartjs-2` - React wrapper for Chart.js
- Chart.js components (CategoryScale, LinearScale, BarElement, etc.)

## File Location
`src/components/Chart/TrafficChart.tsx`
`src/components/Chart/TrafficChart.module.css`

## Testing
- Test with complete data
- Test with null values
- Test with missing data
- Test with very large numbers
- Test responsive behavior
- Test tooltip formatting