if [[ $1 == "" || $1 ==  "-h" ]]; then
  echo "> amplxe.sh mode option url"
  echo "mode: b (browser) s (single) r (render) g (gpu)"
  echo "option: hotspots locksandwaits concurrency advanced-hotspots"
  exit 0
fi

echo "don't forget enabling ptrace"
echo "echo 1 | sudo tee /proc/sys/kernel/yama/ptrace_scope"
echo ""

export url=$3
if [[ $3 ==  "" ]]; then
  export url="http://localhost/browsertests/public/webgl/webgl.html"
fi

echo "mode:"$1" option:"$2" url:"$url
export cmdprefix="amplxe-cl -collect $2"
export basiccmd="./Debug/content_shell --no-sandbox"

if [[ $1 == "b" || $1 == "s" ]]; then
  if [ $1 == "s" ]; then
    export single="--single-process"
  fi
  echo $cmdprefix -- $basiccmd $single $url
  exit 0
elif [[ $1 == "r" ]]; then
  export cmdprocess="--renderer-cmd-prefix"
elif [[ $1 == "g" ]]; then
  export cmdprocess="--gpu-launcher"
fi

echo $basiccmd $url $cmdprocess="'"$cmdprefix"'"
