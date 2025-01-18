#include "M261.h"

void SYS_Init(void)
{
    SYS_UnlockReg();
    
    CLK_EnableXtalRC(CLK_PWRCTL_LIRCEN_Msk|CLK_PWRCTL_HIRCEN_Msk|CLK_PWRCTL_HIRC48EN_Msk);

    CLK_WaitClockReady(CLK_STATUS_LIRCSTB_Msk|CLK_STATUS_HIRCSTB_Msk|CLK_STATUS_HIRC48STB_Msk);
    
    CLK_SetHCLK(CLK_CLKSEL0_HCLKSEL_HIRC, CLK_CLKDIV0_HCLK(1));
    
    CLK->PCLKDIV = (CLK_PCLKDIV_APB0DIV_HCLK | CLK_PCLKDIV_APB1DIV_HCLK);
    
    CLK_EnableModuleClock(BPWM0_MODULE);
    CLK_EnableModuleClock(BPWM1_MODULE);
    CLK_EnableModuleClock(EADC_MODULE);
    CLK_EnableModuleClock(FMCIDLE_MODULE);
    CLK_EnableModuleClock(ISP_MODULE);
    CLK_EnableModuleClock(WDT_MODULE);
    CLK_EnableModuleClock(WWDT_MODULE);
    
    CLK_SetModuleClock(BPWM0_MODULE, CLK_CLKSEL2_BPWM0SEL_PCLK0, MODULE_NoMsk);
    CLK_SetModuleClock(BPWM1_MODULE, CLK_CLKSEL2_BPWM1SEL_PCLK1, MODULE_NoMsk);
    CLK_SetModuleClock(EADC_MODULE, MODULE_NoMsk, CLK_CLKDIV0_EADC(1));
    CLK_SetModuleClock(WDT_MODULE, CLK_CLKSEL1_WDTSEL_LIRC, MODULE_NoMsk);
    CLK_SetModuleClock(WWDT_MODULE, CLK_CLKSEL1_WWDTSEL_HCLK_DIV2048, MODULE_NoMsk);
    
    SystemCoreClockUpdate();
    
    SYS_LockReg();

    return;
}
