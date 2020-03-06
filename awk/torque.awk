###runs only with GAWK
#  25.3531 to  25.8819
BEGIN {#printf "# Time(s) Torque1(N.mm) Torque2(N.mm)\n";  
#printf "#Time(s) Torque1(N.mm) Torque/area*pressure*midradius \n"; pi=3.141592;
area=(pi/4.0)*((715.3**2.0)-(543.1**2.0))
printf "#Time(s) Torque1(N.m) by power/rpm  \n";
pi=3.141592;
}

{
 if( $0 !~ /#/){
#printf "%6.4f    %10.4e    %10.4e \n", $1,
#1000.0*($2*1000.0*60.0)/(2.0*pi*$3),
#6*pi*((209.982**2.0)-(158.115**2.0))*($4/1000.0)*$5*196.85}

#torque=1000.0*($4*1000.0*60.0)/(2.0*pi*$3); 
torque=($3*1000.0*60.0)/(2.0*pi*$2*2.0); # additional two at the end when axle pow
frictional_force=torque/0.25*(715.3+543.1);
printf "%6.4f    %10.4e    \n", $1, torque

             }
}

	

END  { #printf "%02d:%06.3f \n",  int(time/60), time%60
close("tmp_out")}

function scale(N, temp)
{

while( (getline < "tmp_out") !=0){ if( $0 !~ /#/){print $1,$2/temp} }

}


