import { createTheme, Theme } from '@mui/material/styles'
import { ThemeOptions } from '@mui/material/styles'

// McKinsey brand colors
const colors = {
  primary: {
    main: '#0070C0',      // McKinsey Blue
    light: '#4A9BDB',
    dark: '#002E6C',
    contrastText: '#FFFFFF',
  },
  secondary: {
    main: '#00A651',      // McKinsey Green
    light: '#4CBB87',
    dark: '#007A3D',
    contrastText: '#FFFFFF',
  },
  accent: {
    orange: '#FF6B35',
    purple: '#8E44AD',
    yellow: '#F39C12',
    red: '#E74C3C',
    teal: '#1ABC9C',
    navy: '#2C3E50',
  },
  grey: {
    50: '#FAFAFA',
    100: '#F5F5F5',
    200: '#EEEEEE',
    300: '#E0E0E0',
    400: '#BDBDBD',
    500: '#9E9E9E',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
  },
  background: {
    default: '#FAFAFA',
    paper: '#FFFFFF',
    light: '#F8F9FA',
  },
  text: {
    primary: '#212121',
    secondary: '#616161',
    disabled: '#BDBDBD',
  },
  success: {
    main: '#00A651',
    light: '#4CBB87',
    dark: '#007A3D',
  },
  warning: {
    main: '#F39C12',
    light: '#F8C471',
    dark: '#E67E22',
  },
  error: {
    main: '#E74C3C',
    light: '#EC7063',
    dark: '#C0392B',
  },
  info: {
    main: '#0070C0',
    light: '#4A9BDB',
    dark: '#002E6C',
  },
}

// Typography configuration
const typography = {
  fontFamily: [
    'Inter',
    '-apple-system',
    'BlinkMacSystemFont',
    '"Segoe UI"',
    'Roboto',
    '"Helvetica Neue"',
    'Arial',
    'sans-serif',
    '"Apple Color Emoji"',
    '"Segoe UI Emoji"',
    '"Segoe UI Symbol"',
  ].join(','),
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.01562em',
    color: colors.text.primary,
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 700,
    lineHeight: 1.25,
    letterSpacing: '-0.00833em',
    color: colors.text.primary,
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '0em',
    color: colors.text.primary,
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.35,
    letterSpacing: '0.00735em',
    color: colors.text.primary,
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0em',
    color: colors.text.primary,
  },
  h6: {
    fontSize: '1.125rem',
    fontWeight: 600,
    lineHeight: 1.45,
    letterSpacing: '0.0075em',
    color: colors.text.primary,
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 500,
    lineHeight: 1.5,
    letterSpacing: '0.00938em',
    color: colors.text.primary,
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.55,
    letterSpacing: '0.00714em',
    color: colors.text.secondary,
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: '0.00938em',
    color: colors.text.primary,
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: '0.01071em',
    color: colors.text.secondary,
  },
  button: {
    fontSize: '0.875rem',
    fontWeight: 600,
    lineHeight: 1.5,
    letterSpacing: '0.02857em',
    textTransform: 'none' as const,
  },
  caption: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.5,
    letterSpacing: '0.03333em',
    color: colors.text.secondary,
  },
  overline: {
    fontSize: '0.75rem',
    fontWeight: 600,
    lineHeight: 1.5,
    letterSpacing: '0.08333em',
    textTransform: 'uppercase' as const,
    color: colors.text.secondary,
  },
}

// Spacing and layout
const spacing = 8 // Base spacing unit (8px)

const breakpoints = {
  values: {
    xs: 0,
    sm: 600,
    md: 900,
    lg: 1200,
    xl: 1536,
  },
}

// Shadow configuration
const shadows = [
  'none',
  '0px 2px 1px -1px rgba(0,0,0,0.06), 0px 1px 1px 0px rgba(0,0,0,0.04), 0px 1px 3px 0px rgba(0,0,0,0.03)',
  '0px 3px 1px -2px rgba(0,0,0,0.06), 0px 2px 2px 0px rgba(0,0,0,0.04), 0px 1px 5px 0px rgba(0,0,0,0.03)',
  '0px 3px 3px -2px rgba(0,0,0,0.06), 0px 3px 4px 0px rgba(0,0,0,0.04), 0px 1px 8px 0px rgba(0,0,0,0.03)',
  '0px 2px 4px -1px rgba(0,0,0,0.06), 0px 4px 5px 0px rgba(0,0,0,0.04), 0px 1px 10px 0px rgba(0,0,0,0.03)',
  '0px 3px 5px -1px rgba(0,0,0,0.06), 0px 5px 8px 0px rgba(0,0,0,0.04), 0px 1px 14px 0px rgba(0,0,0,0.03)',
  '0px 3px 5px -1px rgba(0,0,0,0.06), 0px 6px 10px 0px rgba(0,0,0,0.04), 0px 1px 18px 0px rgba(0,0,0,0.03)',
  '0px 4px 5px -2px rgba(0,0,0,0.06), 0px 7px 10px 1px rgba(0,0,0,0.04), 0px 2px 16px 1px rgba(0,0,0,0.03)',
  '0px 5px 5px -3px rgba(0,0,0,0.06), 0px 8px 10px 1px rgba(0,0,0,0.04), 0px 3px 14px 2px rgba(0,0,0,0.03)',
  '0px 5px 6px -3px rgba(0,0,0,0.06), 0px 9px 12px 1px rgba(0,0,0,0.04), 0px 3px 16px 2px rgba(0,0,0,0.03)',
  '0px 6px 6px -3px rgba(0,0,0,0.06), 0px 10px 14px 1px rgba(0,0,0,0.04), 0px 4px 18px 3px rgba(0,0,0,0.03)',
  '0px 6px 7px -4px rgba(0,0,0,0.06), 0px 11px 15px 1px rgba(0,0,0,0.04), 0px 4px 20px 3px rgba(0,0,0,0.03)',
  '0px 7px 8px -4px rgba(0,0,0,0.06), 0px 12px 17px 2px rgba(0,0,0,0.04), 0px 5px 22px 4px rgba(0,0,0,0.03)',
  '0px 7px 8px -4px rgba(0,0,0,0.06), 0px 13px 19px 2px rgba(0,0,0,0.04), 0px 5px 24px 4px rgba(0,0,0,0.03)',
  '0px 7px 9px -4px rgba(0,0,0,0.06), 0px 14px 21px 2px rgba(0,0,0,0.04), 0px 5px 26px 4px rgba(0,0,0,0.03)',
  '0px 8px 9px -5px rgba(0,0,0,0.06), 0px 15px 22px 2px rgba(0,0,0,0.04), 0px 6px 28px 5px rgba(0,0,0,0.03)',
  '0px 8px 10px -5px rgba(0,0,0,0.06), 0px 16px 24px 2px rgba(0,0,0,0.04), 0px 6px 30px 5px rgba(0,0,0,0.03)',
  '0px 8px 11px -5px rgba(0,0,0,0.06), 0px 17px 26px 2px rgba(0,0,0,0.04), 0px 6px 32px 5px rgba(0,0,0,0.03)',
  '0px 9px 11px -5px rgba(0,0,0,0.06), 0px 18px 28px 2px rgba(0,0,0,0.04), 0px 7px 34px 6px rgba(0,0,0,0.03)',
  '0px 9px 12px -6px rgba(0,0,0,0.06), 0px 19px 29px 2px rgba(0,0,0,0.04), 0px 7px 36px 6px rgba(0,0,0,0.03)',
  '0px 10px 13px -6px rgba(0,0,0,0.06), 0px 20px 31px 3px rgba(0,0,0,0.04), 0px 8px 38px 7px rgba(0,0,0,0.03)',
  '0px 10px 13px -6px rgba(0,0,0,0.06), 0px 21px 33px 3px rgba(0,0,0,0.04), 0px 8px 40px 7px rgba(0,0,0,0.03)',
  '0px 10px 14px -6px rgba(0,0,0,0.06), 0px 22px 35px 3px rgba(0,0,0,0.04), 0px 8px 42px 7px rgba(0,0,0,0.03)',
  '0px 11px 14px -7px rgba(0,0,0,0.06), 0px 23px 36px 3px rgba(0,0,0,0.04), 0px 9px 44px 8px rgba(0,0,0,0.03)',
  '0px 11px 15px -7px rgba(0,0,0,0.06), 0px 24px 38px 3px rgba(0,0,0,0.04), 0px 9px 46px 8px rgba(0,0,0,0.03)',
] as const

// Component overrides
const components = {
  MuiCssBaseline: {
    styleOverrides: {
      body: {
        backgroundColor: colors.background.default,
        fontSize: '14px',
      },
      '*::-webkit-scrollbar': {
        width: '8px',
        height: '8px',
      },
      '*::-webkit-scrollbar-track': {
        backgroundColor: colors.grey[100],
        borderRadius: '4px',
      },
      '*::-webkit-scrollbar-thumb': {
        backgroundColor: colors.grey[400],
        borderRadius: '4px',
        '&:hover': {
          backgroundColor: colors.grey[500],
        },
      },
    },
  },
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        textTransform: 'none',
        fontWeight: 600,
        fontSize: '0.875rem',
        padding: '8px 16px',
        boxShadow: 'none',
        '&:hover': {
          boxShadow: 'none',
        },
      },
      contained: {
        boxShadow: '0 2px 8px rgba(0, 112, 192, 0.3)',
        '&:hover': {
          boxShadow: '0 4px 12px rgba(0, 112, 192, 0.4)',
        },
      },
      outlined: {
        borderWidth: '1.5px',
        '&:hover': {
          borderWidth: '1.5px',
        },
      },
    },
  },
  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        boxShadow: shadows[1],
        '&:hover': {
          boxShadow: shadows[3],
        },
      },
    },
  },
  MuiPaper: {
    styleOverrides: {
      root: {
        borderRadius: 8,
      },
      elevation1: {
        boxShadow: shadows[1],
      },
      elevation2: {
        boxShadow: shadows[2],
      },
      elevation3: {
        boxShadow: shadows[3],
      },
    },
  },
  MuiTextField: {
    styleOverrides: {
      root: {
        '& .MuiOutlinedInput-root': {
          borderRadius: 8,
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: colors.primary.main,
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderWidth: '2px',
            borderColor: colors.primary.main,
          },
        },
      },
    },
  },
  MuiChip: {
    styleOverrides: {
      root: {
        borderRadius: 6,
        fontWeight: 500,
      },
    },
  },
  MuiAppBar: {
    styleOverrides: {
      root: {
        boxShadow: shadows[1],
      },
    },
  },
  MuiFab: {
    styleOverrides: {
      root: {
        boxShadow: shadows[3],
        '&:hover': {
          boxShadow: shadows[6],
        },
      },
    },
  },
  MuiDialog: {
    styleOverrides: {
      paper: {
        borderRadius: 12,
      },
    },
  },
  MuiMenu: {
    styleOverrides: {
      paper: {
        borderRadius: 8,
        boxShadow: shadows[3],
      },
    },
  },
  MuiTooltip: {
    styleOverrides: {
      tooltip: {
        backgroundColor: colors.grey[800],
        borderRadius: 6,
        fontSize: '0.75rem',
        fontWeight: 500,
      },
    },
  },
}

// Theme options
const themeOptions: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: colors.primary,
    secondary: colors.secondary,
    background: colors.background,
    text: colors.text,
    grey: colors.grey,
    success: colors.success,
    warning: colors.warning,
    error: colors.error,
    info: colors.info,
  },
  typography,
  spacing,
  breakpoints,
  shadows: shadows as any,
  components,
  shape: {
    borderRadius: 8,
  },
}

// Create theme
export const theme: Theme = createTheme(themeOptions)

// Export colors and other utilities
export { colors }

// Utility functions for consistent styling
export const getBoxShadow = (elevation: number) => shadows[elevation] || shadows[1]

export const getPrimaryGradient = () => 
  `linear-gradient(135deg, ${colors.primary.main} 0%, ${colors.primary.dark} 100%)`

export const getSecondaryGradient = () => 
  `linear-gradient(135deg, ${colors.secondary.main} 0%, ${colors.secondary.dark} 100%)`

export const getAccentGradient = (color1: string, color2: string) => 
  `linear-gradient(135deg, ${color1} 0%, ${color2} 100%)`

export default theme