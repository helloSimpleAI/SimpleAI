'use client'

import clsx from 'clsx'
import Link from 'next/link'
import { LogOutIcon } from 'lucide-react'
import { useRouter } from 'next/navigation'

import { Button } from '@/components/Button'
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
import { useApiKey, useUser } from '@/utils/useUser'
import { CopyButton } from '@/components/CopyButton'
import { HeaderSeparator } from '@/components/HeaderUtils'
import { usePostHog } from 'posthog-js/react'
import { obfuscateSecret } from '@/utils/obfuscate'

function CopyableSecret({
  secret = '',
  onAfterCopy,
  obfuscateStart,
  obfuscateEnd,
}: {
  secret: string;
  onAfterCopy: () => void;
  obfuscateStart?: number;
  obfuscateEnd?: number;
}) {
  return (
    <>
      <span className="whitespace-nowrap font-mono text-yellow-400 group-hover:opacity-25">
        {obfuscateSecret(secret, obfuscateStart, obfuscateEnd)}
      </span>
      <span className="absolute inset-0">
        <CopyButton
          code={secret}
          onAfterCopy={onAfterCopy}
          customPositionClassNames={clsx(
            'top-[-2px] bottom-[2px]' /* nudge 2px up*/,
            'left-[-6px] right-[-6px]' /* widen a little to fit nicely */,
            'min-h-[28px]',
          )}
        />
      </span>
    </>
  )
}

export const Auth = function () {
  const { user, isLoading, error } = useUser()
  const apiKey = useApiKey()
  const posthog = usePostHog()
  const router = useRouter()
  const supabase = createClientComponentClient()

  async function signOut() {
    await supabase.auth.signOut()
    posthog?.reset(true)
    router.push('/')
    window.location.reload()
  }

  function redirectToCurrentURL() {
    const url = typeof window !== 'undefined' ? window.location.href : undefined

    if (!url) {
      return ''
    }

    const encodedURL = encodeURIComponent(url)
    return `redirect_to=${encodedURL}`
  }


  if (error)
    return (
      <div className="flex flex-row items-center gap-4">
        <span className="text-sm text-red-500" title={error?.message}>
          Something went wrong
        </span>
        <Link href={`/sign-in?${redirectToCurrentURL()}`}>
          <Button>Sign In</Button>
        </Link>
      </div>
    )

  if (isLoading)
    return (
      <div className="flex animate-pulse">
        <div title="Loading..." className="h-2 w-40 rounded bg-slate-500"></div>
      </div>
    )

  return (
    <>
      {user ? (
        <div className="flex flex-col items-center gap-4 min-[540px]:flex-row">
          <div
            className="
              group relative flex
              flex-row
              gap-2 text-xs
            "
          >
            <span className="whitespace-nowrap font-bold text-zinc-400 group-hover:opacity-25">
              API Key
            </span>
            <CopyableSecret
              secret={apiKey}
              onAfterCopy={() => posthog?.capture('copied API key')}
            />
          </div>
          <HeaderSeparator />
          <div className="flex items-center gap-2">
            <div className="whitespace-nowrap text-xs font-bold">
              {user.email}
            </div>
            {/* @ts-ignore */}
            <Button
              variant="textSubtle"
              title="Sign out"
              onClick={() => signOut()}
            >
              <LogOutIcon className="h-5 w-5" />
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-center gap-3">
          <Link href={`/sign-in?view=sign-up&${redirectToCurrentURL()}`}>
            <Button
              variant="textTernary"
              className="whitespace-nowrap text-xs"
            >
              Sign up to get your API key
            </Button>
          </Link>

          <Link href={`/sign-in?${redirectToCurrentURL()}`}>
            <Button>Sign In</Button>
          </Link>
        </div>
      )}
    </>
  )
}
